from typing import List

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?\
                        check_same_tread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def today_tasks(session, Table):
    tasks = session.query(Table).filter(Table.deadline == \
                                        datetime.today().date()).all()

    if tasks:
        print(f'Today {datetime.today().day} \
{datetime.today().strftime("%b")}:')
        count = 1
        for task in tasks:
            print(count, ". ", task, sep='')
            count += 1
    else:
        print("Nothing to do!")
    print()


def week_tasks(session, Table):
    weekday = datetime.today().date().weekday()

    """tasks = session.query(Table).filter(Table.deadline >= \
            (datetime.today().date()), \
            (Table.deadline < (datetime.today().date() + timedelta(days=6)))).order_by(Table.deadline).all()"""

    weekdays: list[str] = ['Sunday', 'Monday', "Tuesday", 'Wednesday', \
                           'Thursday', 'Friday', 'Saturday']
    for i in range(7):
        tasks = session.query(Table).filter(Table.deadline == \
                (datetime.today().date() + timedelta(days=(i)))).all()

        print(weekdays[(weekday + i + 1) % 7], ' ',\
              (datetime.today() + timedelta(days=(i))).day, ' ', \
              datetime.today().strftime('%b'), ':', sep='')
        if tasks:
            count = 1

            for task in tasks:
                print(count, ". ", task, sep='')
                count += 1
        else:
            print("Nothing to do!")
        print()


def all_tasks(session, Table):
    tasks = session.query(Table).order_by(Table.deadline).all()
    print("All tasks:")
    count = 1
    for task in tasks:
        print(count,'. ', task, '.', ' ',\
              (task.deadline).day, ' ',\
              task.deadline.strftime('%b'), sep='')
        count += 1
    print()


def add_new_task(session, Table):
    print('Enter task')
    task = input()
    print('Enter deadline')
    date = datetime.strptime(input(), '%Y-%m-%d')
    new_task = Table(task=task, deadline=date)
    session.add(new_task)
    session.commit()
    print('The task has been added!')
    print()


def missed_tasks(session, Table):
    tasks = session.query(Table).\
        filter(Table.deadline < datetime.today().date()).\
        order_by(Table.deadline).all()
    print("Missed tasks:")
    if tasks:
        count = 1
        for task in tasks:
            print(count, '. ', task, '.', ' ', \
                  (task.deadline).day, ' ', \
                  task.deadline.strftime('%b'), sep='')
            count += 1
    else:
        print("Nothing is missed!")
    print()


def delete_task(session, Table):
    tasks = session.query(Table).order_by(Table.deadline).all()
    print("Choose the number of the task you want to delete:")
    count = 1
    for task in tasks:
        print(count, '. ', task, '.', ' ', \
              (task.deadline).day, ' ', \
              task.deadline.strftime('%b'), sep='')
        count += 1
    number_for_delete = int(input()) - 1

    session.delete(tasks[number_for_delete])
    session.commit()
    print('The task has been deleted!')
    print()


if __name__ == '__main__':

    while True:
        print("1) Today's tasks\n2) Week's tasks\n3) All tasks")
        print("4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
        choise = int(input())
        if choise == 1:
            today_tasks(session, Table)

        elif choise == 2:
            print()
            week_tasks(session, Table)
        elif choise == 3:
            all_tasks(session, Table)
        elif choise == 4:
            missed_tasks(session,Table)
        elif choise == 5:
            add_new_task(session, Table)
        elif choise == 6:
            delete_task(session, Table)
        elif choise == 0:
            print("Bye")
            break
