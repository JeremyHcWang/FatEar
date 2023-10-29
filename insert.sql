INSERT INTO user (username, pwd, fname, lname, lastlogin, nickname) 
VALUES ('mw301', 'marquis301', 'Marquis', 'Warren', '2023-01-23', 'The Bounty Hunter'),
       ('jr426', 'john426', 'John', 'Ruth', '2023-03-21', 'The Hangman'),
       ('dd401', 'daisy401', 'Daisy', 'Doumergue', '2023-01-15', 'The Prisoner'),
       ('cm701', 'chris701', 'Chris', 'Meninx', '2022-09-08', 'The New Sheriff'),
       ('sb505', 'senor505', 'Senor', 'Bob', '2023-03-23', 'The Foreigner'),
       ('om328', 'oswaldoy328', 'Oswaldo', 'Mobray', '2023-03-29', 'The Little Man'),
       ('jg401', 'joe401', 'Joe', 'Gage', '2022-12-31', 'The Cowboy');

INSERT INTO song (songID, title, releaseDate, songURL)
VALUES ('s001', 'Savior', '2022-05-13', 'https://g.co/kgs/PnzHhW'),
       ('s002', 'Die Hard', '2022-05-13', 'https://g.co/kgs/FmzwCd'),
       ('s003', 'United In Grief', '2022-05-13', 'https://g.co/kgs/C7BGT7'),
       ('s004', 'Love Me Now', '2023-12-06', 'https://g.co/kgs/Niw7Tq'),
       ('s005', 'I Know Better', '2016-12-06', 'https://g.co/kgs/fUpbEN'),
       ('s006', 'Shape of You', '2017-03-03', 'https://g.co/kgs/cMJD8o'),
       ('s007', 'Galway Girl', '2017-03-03', 'https://g.co/kgs/WoBufG'),
       ('s008', 'Castle on the Hill', '2017-03-03', 'https://g.co/kgs/Ds21Ur'),
       ('s009', 'Love Yourself', '2015-11-13', 'https://g.co/kgs/FNL2cu'),
       ('s010', 'Sorry', '2015-11-13', 'https://g.co/kgs/Jk6xF4'),
       ('s011', 'I’ll Show You', '2015-11-13', 'https://g.co/kgs/otFSGk');

INSERT INTO artist (artistID, fname, lname, artistBio, artistURL)
VALUES ('a001', 'John', 'Legend', 'John Legend is a singer, songwriter, and actor.', 'https://www.johnlegend.com/'),
       ('a002', 'Kendrick', 'Lamar', 'Kendrick Lamar is an American rapper and songwriter', 'https://oklama.com/'),
       ('a003', 'Ed', 'Sheeran', 'Ed Sheeran is an English singer and songwriter.', 'https://www.edsheeran.com/'),
       ('a004', 'Justin', 'Bieber', 'Justin Drew Bieber is a Canadian singer.', 'https://www.justinbiebermusic.com/');

INSERT INTO album (albumID)
VALUES ('al001'), ('al002'), ('al003'), ('al004');

INSERT INTO friend (user1, user2, acceptStatus, requestSentBy, createdAt, updatedAt)
VALUES ('mw301', 'dd401', 'Accepted', 'mw301', '2021-03-01', '2022-05-01'),
       ('mw301', 'sb505', 'Pending', 'mw301', '2021-03-01', '2022-05-01'),
       ('mw301', 'jg401', 'Denied', 'jg401', '2021-03-01', '2022-05-01'),
       ('mw301', 'om328', 'Accepted', 'mw301', '2021-03-01', '2022-05-01'),
       ('sb505', 'cm701', 'Accepted', 'sb505', '2021-04-01', '2022-04-01'),
       ('sb505', 'jg401', 'Accepted', 'sb505', '2021-04-01', '2022-04-01');

INSERT INTO follows (follower, follows, createdAt)
VALUES ('jr426', 'dd401', '2022-03-31'),
       ('jr426', 'cm701', '2022-04-30'),
       ('jr426', 'om328', '2022-05-29'),
       ('cm701', 'jr426', '2022-05-28'),
       ('cm701', 'sb505', '2022-06-28'),
       ('om328', 'sb505', '2022-06-28'),
       ('om328', 'jr426', '2022-08-28'),
       ('om328', 'jg401', '2022-10-28'),
       ('mw301', 'jg401', '2022-10-28');

INSERT INTO rateAlbum (username, albumID, stars)
VALUES ('dd401', 'al001', 4),
       ('cm701', 'al001', 5),
       ('jg401', 'al002', 3);

INSERT INTO reviewAlbum (username, albumID, reviewText, reviewDate)
VALUES ('dd401', 'al001', 'Great album!', '2023-03-01'),
       ('dd401', 'al002', 'Great album!', '2023-01-01');

INSERT INTO rateSong(username, songID, stars, ratingDate)
VALUES ('dd401', 's001', 4, '2022-03-01'),
       ('dd401', 's002', 5, '2023-03-02'),
       ('cm701', 's003', 2, '2023-03-03'),
       ('jg401', 's002', 3, '2023-01-01'),
       ('jg401', 's003', 3, '2023-03-04'),
       ('jg401', 's009', 1, '2023-03-05');

INSERT INTO reviewSong(username, songID, reviewText, reviewDate)
VALUES ('dd401', 's001', 'Great song!', '2023-03-01'),
       ('dd401', 's002', 'Love it!', '2023-03-02'),
       ('cm701', 's001', 'Not my favorite', '2023-03-03'),
       ('jg401', 's003', 'It is okay', '2023-03-04'),
       ('jg401', 's004', 'Terrible', '2023-03-05');

INSERT INTO songInAlbum(albumID, songID)
VALUES ('al001', 's001'),
       ('al001', 's002'),
       ('al001', 's003'),
       ('al002', 's004'),
       ('al002', 's005'),
       ('al003', 's006'),
       ('al003', 's007'),
       ('al003', 's008'),
       ('al004', 's009'),
       ('al004', 's010'),
       ('al004', 's011');

INSERT INTO songGenre(songID, genre)
VALUES ('s001', 'Hip Hop'),
       ('s002', 'Hip Hop'),
       ('s003', 'Hip Hop'),
       ('s004', 'Jazz'),
       ('s005', 'Jazz'),
       ('s006', 'Pop'),
       ('s007', 'Pop'),
       ('s008', 'Pop'),
       ('s009', 'Hip Hop'),
       ('s010', 'Pop'),
       ('s011', 'Pop');

INSERT INTO artistPerformsSong(artistID, songID)
VALUES ('a002', 's001'),
       ('a002', 's002'),
       ('a002', 's003'),
       ('a001', 's004'),
       ('a001', 's005'),
       ('a003', 's006'),
       ('a003', 's007'),
       ('a003', 's008'),
       ('a004', 's009'),
       ('a004', 's010'),
       ('a004', 's011');

INSERT INTO userFanOfArtist(username, artistID)
VALUES ('mw301', 'a001'),
       ('sb505', 'a002'),
       ('cm701', 'a003');