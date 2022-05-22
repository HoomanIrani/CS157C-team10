# CS157C-team10

# Student Opinion: Feedback System for Universities

## Goal

Purpose of this project simply is to create an in-house platform for universities to design, collect, analyze and report student’s feedback to professors over multiple courses of time during a semester or quarter. This platform lets university’s coordinators design appropriants. This method provides lots of flexibility that is usually rare in the university’s feedback system. 

## Motivation

Motivation behind this idea is to create an independent platform to be used by institutes, colleges and universities which provide them an easy to use platform that is configurable and can be designed based on the institutes need. Platform then automatically analyzes and reports the data to both instructors and university’s coordinators for improving academics during the semester. One big problem with most surveys that universities provide is that they are all the same and not specific toward a course or major. The other problem is that they are usually held at the end of the semester which is absolutely fine to provide feedback for both professors and coordinators but students will not have any benefit here. This system improves all these issues and provides a more flexible mechanism for all party members.

## Stakeholders

Stakeholders involved in this project are students, professors and coordinators respectively. Coordinators are the one that design the survey forms based on the course needs. In the next step students are asked to fill the forms. Once the survey is finished, professors receive the feedback results and statistical data based on the students survey. Coordinators also can see the results to make sure how instructors perform.

## Functional Requirements:
### Users
#### Student
Login to available feedback forms using their username/password <br>
Fill in feedback forms for faculties once they logged in <br>
#### Coordinator
Login to see coordinator dashboard<br>
Create and publish feedback forms<br>
They can access all feedback results<br>
#### Professor
Login to see professor dashboard<br>
Analysis of received feedback<br>
Overall feedback received<br>
Ability to see past feedbacks<br>

## Features
Web-based application: Creating a Django (Python) based web application. Changes will be made and applied centrally (no executable file). All users will use one version of the application. Users will be able to access this application from any browser (computer, phone, tablet, etc).<br>
Analytical dashboard for professors: Visualizing data (feedback) for better understanding.<br>
Apache Cassandra: To filter and query feedback received from students using CQL (Cassandra Query Language) to create analytics and reports for the professor dashboard.<br> 

## Functions

Anonymous feedback from students: Faculty can only see comments, compliments and reviews from students. The students' identities will be hidden from professor’s.<br>
Control over questions: Coordinator can add/remove questions upon requests from professors. <br>
Overall improvement graph: Feedbacks can be conducted multiple times over a semester. Professors can see them.<br>

## Steps to execute:
#### Install docker<br>
We need to run a separate container of cassandra in docker as cassandra requires python2 but our project is in python3. Running cassandra in docker gives us the flexibility to focus our dependencies of the project.<br>

Pull latest Cassandra image and run it in the background: <br>
Commands:<br>
docker pull cassandra:latest <br>
docker run -d --name cassandra-docker -p 9042:9042 cassandra<br>

#### Open CQLSH to view and execute queries:
Open cqlsh and create keyspace db<br />
Command:<br />
docker exec -i -t cassandra-docker cqlsh<br />
CREATE KEYSPACE db WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 1};<br />

#### Install python dependencies:<br />
Commands:<br />
pip install Django==2.2.1<br />
pip install vaderSentiment<br />
pip install word-forms<br />
pip install nltk<br />
#### Sync and prepopulate the database using python django shell:<br />
Create tables based on models.py using command:<br />
python manage.py migrate --run-syncdb<br />

#### Sync cassandra tables:
python manage.py sync_cassandra<br />

#### Open shell and run the database population scripts: 
To create users for student, coordinator and professor we have created a script called as db_gen.py when you import this script using shell all the commands related to creating users will be executed. We have one more script called as db_populate.py, this script will generate all the entries for feedback form, questions, tags and also will populate feedback responses randomly for the created students.<br />
Commands:<br />
python manage.py shell<br />
import db_gen<br />
import db_populate<br />

#### Run the django server:
To run the server:<br />
python manage.py runserver<br />

