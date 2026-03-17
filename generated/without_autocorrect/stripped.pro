game(billiards).
game('snooker').
billiard_variant('snooker').
word('snooker').

person('Sir Neville Chamberlain').
title('Sir Neville Chamberlain', sir).
rank('Sir Neville Chamberlain', colonel).

person('John Roberts').
champion('John Roberts', billiards, 1885).
british('John Roberts').

person(pm1).
english(pm1).
prime_minister(pm1).
future(pm1, prime_minister).
namesake('Sir Neville Chamberlain', pm1).

time(t1).
end(t1).
century(t1, 19).

time(t2).
later_than(t2, t1).

time(t3).
later_than(t3, t2).

appeared('snooker', 'India', 1875).

very_widespread(billiards, Person, t1) :-
    english(Person),
    officer(Person),
    served_in(Person, 'India', t1).

proposal(proposal1).
proposer(proposal1, 'Sir Neville Chamberlain').
action(proposal1, add).
object(proposal1, balls).
color(balls, colored).
target(proposal1, billiards).
time(proposal1, t1).

slang('snooker', military, t1).

means('snooker', Person) :-
    cadet(Person),
    serves_year(Person, first).

version(version1).
one(version1).
says(version1, call1).

utterance(call1).
caller(call1, 'Sir Neville Chamberlain').
target(call1, opponent1).
word_used(call1, 'snooker').
time(call1, t1).
reason(call1, situation1).

person(opponent1).
opponent_of(opponent1, 'Sir Neville Chamberlain').
stuck(opponent1, situation1).

situation(situation1).
difficult(situation1).
formed_on(situation1, table).

possible(called(Person, 'snooker')) :-
    beginner(Person),
    begins(Person, 'snooker').

type(Position, 'snooker') :-
    position(Position),
    on(Position, table),
    required(Ball),
    direct_hit(Position, Ball, impossible).

denotes_at('snooker', Position, t2) :-
    type(Position, 'snooker').

denotes_at('snooker', 'snooker', t3).

new('snooker', telling1).

journey(journey1).
traveler(journey1, 'John Roberts').
location(journey1, 'India').
year(journey1, 1885).

meeting(meeting1).
participant(meeting1, 'John Roberts').
participant(meeting1, 'Sir Neville Chamberlain').
location(meeting1, 'India').
year(meeting1, 1885).

telling(telling1).
speaker(telling1, 'Sir Neville Chamberlain').
listener(telling1, 'John Roberts').
topic(telling1, 'snooker').
year(telling1, 1885).
after(meeting1, telling1).

spread(spread1).
agent(spread1, 'John Roberts').
object(spread1, 'snooker').
location(spread1, 'England').
after(telling1, spread1).

appeared_in(Thing, Place) :-
    appeared(Thing, Place, _).

champion(Person, Game) :-
    champion(Person, Game, _).

very_widespread(Game, Person) :-
    very_widespread(Game, Person, _).

called_in(Version, Person, Word) :-
    says(Version, Utterance),
    target(Utterance, Person),
    word_used(Utterance, Word).

traveled(Person, Place, Year) :-
    journey(Journey),
    traveler(Journey, Person),
    location(Journey, Place),
    year(Journey, Year).

met(Person1, Person2) :-
    meeting(Meeting),
    participant(Meeting, Person1),
    participant(Meeting, Person2),
    Person1 \= Person2.

met_in(Person1, Person2, Place) :-
    meeting(Meeting),
    participant(Meeting, Person1),
    participant(Meeting, Person2),
    location(Meeting, Place),
    Person1 \= Person2.

told_about(Speaker, Listener, Topic) :-
    telling(Telling),
    speaker(Telling, Speaker),
    listener(Telling, Listener),
    topic(Telling, Topic).

spread(Person, Thing, Place) :-
    spread(Event),
    agent(Event, Person),
    object(Event, Thing),
    location(Event, Place).

denotes(Word, Meaning) :-
    denotes_at(Word, Meaning, _).
