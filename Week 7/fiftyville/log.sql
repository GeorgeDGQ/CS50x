-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Jorge Daniel Gómez Quintana "Fifyville"
SELECT description FROM crime_scene_reports WHERE day=28 AND street='Humphrey Street';
SELECT transcript FROM interviews WHERE day=28;

SELECT name FROM people WHERE license_plate IN (
    SELECT license_plate FROM bakery_security_logs WHERE day=28 AND activity='exit' AND hour=10 AND minute>15 AND minute<25
);

SELECT name FROM people WHERE id IN (
    SELECT person_id FROM bank_accounts WHERE account_number IN (
        SELECT account_number FROM atm_transactions WHERE transaction_type='withdraw' AND day=28 AND atm_location='Leggett Street'
    )
);

SELECT name FROM people WHERE phone_number IN (
    SELECT caller FROM phone_calls WHERE day=28 AND duration<60
);

SELECT name FROM people WHERE phone_number IN (
    SELECT receiver FROM phone_calls WHERE day=28 AND duration<60
);

SELECT id FROM flights WHERE origin_airport_id= (SELECT id FROM airports WHERE city='Fiftyville') AND day=29
    ORDER BY hour, minute
        LIMIT 1;

SELECT name FROM people WHERE passport_number IN (
    SELECT passport_number FROM passengers WHERE flight_id=36
);

SELECT p.name FROM people p
INNER JOIN passengers ps ON p.passport_number = ps.passport_number AND ps.flight_id = 36
INNER JOIN phone_calls pc ON p.phone_number = pc.caller AND pc.day = 28 AND pc.duration < 60
INNER JOIN bakery_security_logs bsl ON p.license_plate = bsl.license_plate AND bsl.day = 28 AND bsl.activity = 'exit' AND bsl.hour = 10 AND bsl.minute > 15 AND bsl.minute < 25
INNER JOIN bank_accounts ba ON p.id = ba.person_id
INNER JOIN atm_transactions atm ON ba.account_number = atm.account_number AND atm.transaction_type = 'withdraw' AND atm.day = 28 AND atm.atm_location = 'Leggett Street';

SELECT name FROM people WHERE phone_number IN (
    SELECT receiver FROM phone_calls WHERE day=28 AND duration<60 AND caller = (
        SELECT phone_number FROM people WHERE name='Bruce'
    )
);
