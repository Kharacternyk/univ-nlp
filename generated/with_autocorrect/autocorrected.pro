% Basic entities
game(snooker).
game(billiards).

country('Індія').
country('Англія').

person('Невілл Чемберлен').
person('Джон Робертс').
person(opponent_1).

office(prime_minister).

period(period_1).
period(period_2).
period(period_3).

group(group_1).

state(state_1).

collection(balls_1).

version(version_1).

class(cadet).
class(novice).

position(position_1).
position(position_2).

hit(hit_1).

ball(ball_1).

event(event_1).
event(event_2).
event(event_3).
event(event_4).
event(event_5).
event(event_6).

% Titles, roles, and identities
word('снукер').

rank('Невілл Чемберлен', colonel).
title('Невілл Чемберлен', sir).

officer(Person) :- rank(Person, colonel).

champion('Джон Робертс', billiards, british).

nationality(prime_minister, english).
nationality(group_1, english).

time_status(prime_minister, future).
namesake('Невілл Чемберлен', prime_minister).

role(group_1, officer).
opponent_of(opponent_1, 'Невілл Чемберлен').

service_year(cadet, first).
beginning_to_play(novice, snooker).

variety_of(snooker, billiards).

% Period properties and temporal relations
century(period_1, 19).
phase(period_1, end).

after(period_2, period_1).
after(period_3, period_2).
after(period_3, period_1).
after(event_5, event_4).
after(event_6, event_5).
after(event_6, event_4).

during(state_1, period_1).
during(event_1, period_1).
during(event_2, period_1).

year(event_3, 1885).
year(event_4, 1885).
year(event_5, 1885).

appeared(snooker, 'Індія', 1875).
status(snooker, new, 1885).

% Context, objects, and positions
served_in(group_1, 'Індія', period_1).

relation(state_1, widespread).
subject(state_1, billiards).
audience(state_1, group_1).
degree(state_1, very).

item_type(balls_1, ball).
color(balls_1, colored).

attribute(position_1, difficult).

on(position_1, table).
on(position_2, table).

cannot_exit(opponent_1, position_1).

direct(hit_1).

target(event_1, billiards).
target(hit_1, ball_1).

impossible(hit_1).
in(hit_1, position_2).
required(ball_1).

% Word origin and meanings
slang('снукер', military, period_1).

refers('снукер', cadet, period_1).
refers('снукер', novice, possible).
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

% Events and their participants
kind(event_1, proposal).
kind(event_2, calling).
kind(event_3, travel).
kind(event_4, meeting).
kind(event_5, telling).
kind(event_6, spreading).

actor(event_1, 'Невілл Чемберлен').
actor(event_2, 'Невілл Чемберлен').
actor(event_3, 'Джон Робертс').
actor(event_5, 'Невілл Чемберлен').
actor(event_6, 'Джон Робертс').

action(event_1, add).

object(event_1, balls_1).
object(event_6, snooker).

patient(event_2, opponent_1).

according_to(event_2, version_1).

participant(event_4, 'Джон Робертс').
participant(event_4, 'Невілл Чемберлен').

recipient(event_5, 'Джон Робертс').
topic(event_5, snooker).

place(event_1, 'Індія').
place(event_3, 'Індія').
place(event_4, 'Індія').
place(event_5, 'Індія').
place(event_6, 'Англія').