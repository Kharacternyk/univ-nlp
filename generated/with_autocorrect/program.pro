% Basic entities
game(snooker).
game(billiards).
country('Індія').
country('Англія').
person('Невілл Чемберлен').
person('Джон Робертс').
word('снукер').

% Titles and roles
rank('Невілл Чемберлен', colonel).
title('Невілл Чемберлен', sir).
officer(Person) :- rank(Person, colonel).

champion('Джон Робертс', billiards, british).

office(prime_minister).
nationality(prime_minister, english).
time_status(prime_minister, future).
namesake('Невілл Чемберлен', prime_minister).

% Time periods
period(period_1).
century(period_1, 19).
phase(period_1, end).

period(period_2).
after(period_2, period_1).

period(period_3).
after(period_3, period_2).
after(period_3, period_1).

% Origin of snooker and billiards context
appeared(snooker, 'Індія', 1875).

group(group_1).
role(group_1, officer).
nationality(group_1, english).
served_in(group_1, 'Індія', period_1).

state(state_1).
relation(state_1, widespread).
subject(state_1, billiards).
audience(state_1, group_1).
during(state_1, period_1).
degree(state_1, very).

event(event_1).
kind(event_1, proposal).
actor(event_1, 'Невілл Чемберлен').
action(event_1, add).
object(event_1, balls_1).
target(event_1, billiards).
place(event_1, 'Індія').
during(event_1, period_1).

collection(balls_1).
item_type(balls_1, ball).
color(balls_1, colored).

% Military slang and one version of the name origin
slang('снукер', military, period_1).

class(cadet).
service_year(cadet, first).
refers('снукер', cadet, period_1).

version(version_1).

event(event_2).
kind(event_2, calling).
actor(event_2, 'Невілл Чемберлен').
patient(event_2, opponent_1).
term(event_2, 'снукер').
according_to(event_2, version_1).
during(event_2, period_1).

person(opponent_1).
opponent_of(opponent_1, 'Невілл Чемберлен').
cannot_exit(opponent_1, position_1).

position(position_1).
attribute(position_1, difficult).
on(position_1, table).

class(novice).
beginning_to_play(novice, snooker).
refers('снукер', novice, possible).

% Later meanings of the word
position(position_2).
on(position_2, table).

hit(hit_1).
direct(hit_1).
target(hit_1, ball_1).
impossible(hit_1).
in(hit_1, position_2).

ball(ball_1).
required(ball_1).

refers('снукер', Position, period_2) :-
    position(Position),
    on(Position, table),
    hit(Hit),
    direct(Hit),
    target(Hit, Ball),
    impossible(Hit),
    in(Hit, Position),
    ball(Ball),
    required(Ball).

refers('снукер', snooker, period_3).
variety_of(snooker, billiards).

% John Roberts and the spread of snooker in England
event(event_3).
kind(event_3, travel).
actor(event_3, 'Джон Робертс').
place(event_3, 'Індія').
year(event_3, 1885).

event(event_4).
kind(event_4, meeting).
participant(event_4, 'Джон Робертс').
participant(event_4, 'Невілл Чемберлен').
place(event_4, 'Індія').
year(event_4, 1885).

event(event_5).
kind(event_5, telling).
actor(event_5, 'Невілл Чемберлен').
recipient(event_5, 'Джон Робертс').
topic(event_5, snooker).
place(event_5, 'Індія').
year(event_5, 1885).
status(snooker, new, 1885).
after(event_5, event_4).

event(event_6).
kind(event_6, spreading).
actor(event_6, 'Джон Робертс').
object(event_6, snooker).
place(event_6, 'Англія').
after(event_6, event_5).
after(event_6, event_4).