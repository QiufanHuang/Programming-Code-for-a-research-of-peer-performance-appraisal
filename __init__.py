
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'PPA_Game'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 3
    MULTIPLIER = 100
class Subsession(BaseSubsession):
    pass
def set_group(subsession: Subsession):
    session = subsession.session
    if subsession.round_number==1:
        new_structure = [[1,2],[3,4]]
        subsession.set_group_matrix(new_structure)
    if subsession.round_number==2:
        new_structure = [[1,3],[2,4]]
        subsession.set_group_matrix(new_structure)
    if subsession.round_number==3:
        new_structure = [[1,4],[2,3]]
        subsession.set_group_matrix(new_structure)
class Group(BaseGroup):
    rate_sum = models.IntegerField()
    group_score = models.IntegerField(initial=0)
    group_bonus = models.IntegerField()
    total_rates = models.IntegerField()
    Group_label = models.StringField(initial='Your group members and a sentence each of them shared: <p></p>')
def set_group_score(group: Group):
    players = group.get_players()
    for player in players:
        if player.answer_1==1:player.score=player.score+1
        if player.answer_2==1:player.score=player.score+1
        if player.answer_3==1:player.score=player.score+1
        if player.answer_4==1:player.score=player.score+1
        if player.answer_5==1:player.score=player.score+1
    scores=[p.score for p in players]
    group.group_score=sum(scores)
    group.group_bonus=C.MULTIPLIER*group.group_score
    for player in players:
        player.teammate_score=group.group_score-player.score
def set_group_bonus(group: Group):
    players = group.get_players()
    rates =[p.rate for p in players]
    group.total_rates=sum(rates)
    for player in players:
        player.teammate_rate=group.total_rates-player.rate
        player.player_gain=group.group_bonus*0.25+group.group_bonus*0.25*(group.total_rates-player.rate)/group.total_rates*2
        if group.group_bonus!=0:player.player_percentage=player.player_gain/group.group_bonus*100 
        else:player.player_percentage=0
        player.player_gain=round(player.player_gain,2)
        player.player_percentage=round(player.player_percentage,2)
def set_nickname_comments(group: Group):
    players = group.get_players()
    
    for player in players:
        p=player.player_nickname+":"+player.player_comments+'<p></p>'
        group.Group_label=group.Group_label+p
    
class Player(BasePlayer):
    player_nickname = models.StringField(label='Please enter your Nickname')
    player_comments = models.StringField(label='Please enter a sentence: Something you want to tell your teammate before the game.')
    score = models.IntegerField(initial=0)
    rate = models.IntegerField(label="Please rate your teammate's performance from 1 to 10.", max=10, min=1)
    teammate_score = models.IntegerField()
    answer_1 = models.IntegerField(blank=True, choices=[[5, 'A'], [4, 'B'], [3, 'C'], [2, 'D'], [1, 'E']], initial=0, label='Please select your answer for question 1 ', widget=widgets.RadioSelect)
    answer_2 = models.IntegerField(blank=True, choices=[[1, 'A'], [2, 'B'], [3, 'C'], [4, 'D'], [5, 'E']], initial=0, label='Please select your answer for question 2', widget=widgets.RadioSelect)
    answer_3 = models.IntegerField(blank=True, choices=[[5, 'A'], [3, 'B'], [1, 'C'], [2, 'D'], [4, 'E']], initial=0, label='Please select your answer for question 3', widget=widgets.RadioSelect)
    answer_4 = models.IntegerField(blank=True, choices=[[5, 'A'], [3, 'B'], [2, 'C'], [1, 'D'], [4, 'E']], initial=0, label='Please select your answer for question 4', widget=widgets.RadioSelect)
    answer_5 = models.IntegerField(blank=True, choices=[[2, 'A'], [1, 'B'], [3, 'C'], [4, 'D'], [5, 'E']], initial=0, label='Please select your answer for question 5', widget=widgets.RadioSelect)
    question_set = models.IntegerField(choices=[[1, 'A'], [2, 'B']], label='Please enter the question set that you choose', widget=widgets.RadioSelect)
    player_gain = models.FloatField()
    player_percentage = models.FloatField()
    trusted = models.IntegerField(label='Please enter the degree that you feel being trusted by your teammates in this round of game. ', max=10, min=1)
    trust = models.IntegerField(label='Please enter the degree that you trust your teammates in this round of game. ')
    cooperation = models.IntegerField(label='Please enter the degree of cooperative behaviours that you perceived in this round.', max=10, min=1)
    will_cooperate = models.IntegerField(label='Please enter the degree of your willingness to cooperate afterwards. ', max=10, min=1)
    rate_next = models.IntegerField(label='After acknowledging your final share of the bonus ,if you have a second chance to rate this game, what mark will you give to your teammates.', max=10, min=1)
    satisfaction = models.IntegerField(label='Please enter your overall satisfaction about the bonus share you finally get.', max=10, min=1)
    email = models.LongStringField(blank=True, initial='', label='Please enter your email here. ')
    teammate_rate = models.IntegerField()
def get_player_total_score(player: Player):
    pass
def custom_export(players):
    yield ['participant_code', 'id_in_group']
    for p in players:
        pp = p.participant
        yield [pp.code, p.id_in_group]
class Group_Wait_Page(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = set_group
class Before_game(Page):
    form_model = 'player'
    form_fields = ['player_nickname', 'player_comments']
class Wait_before_game(WaitPage):
    after_all_players_arrive = set_nickname_comments
class Beginning(Page):
    form_model = 'player'
    form_fields = ['question_set']
class Waitpage1(WaitPage):
    pass
class Task(Page):
    form_model = 'player'
    form_fields = ['answer_1', 'answer_2', 'answer_3', 'answer_4', 'answer_5']
    timeout_seconds = 360
class Waitpage2(WaitPage):
    after_all_players_arrive = set_group_score
class Appraisal(Page):
    form_model = 'player'
    form_fields = ['rate']
class Waitpage3(WaitPage):
    after_all_players_arrive = set_group_bonus
class Survey_after(Page):
    form_model = 'player'
    form_fields = ['trusted', 'trust', 'cooperation', 'will_cooperate', 'rate_next', 'satisfaction']
class Round_End(Page):
    form_model = 'player'
    form_fields = ['email']
page_sequence = [Group_Wait_Page, Before_game, Wait_before_game, Beginning, Waitpage1, Task, Waitpage2, Appraisal, Waitpage3, Survey_after, Round_End]