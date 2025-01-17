import copy as cp
from gender import Gender
from personality import Personality
from user import User
import statistics as st


class Team:
    """This class represents a single team consisting of at least 2 users"""
    # Constructor
    # This takes a list of users as argument

    def __init__(self, userslist: list):
        self.userslist = cp.deepcopy(userslist)

    # performance function based on gender, here no normalization required because we focus on
    # the normalization when we sum performance (this to be done in a seperate class which has an aggregate
    # of teams)
    # Important: We focus on diversifying gender here
    def gender_performance(self) -> float:
        num_of_males = 0
        num_of_females = 0
        for person in self.userslist:
            if (person.gender.value == -1):  # male case
                num_of_males = num_of_males + person.gender.value
            if (person.gender.value == 1):  # female case
                num_of_females = num_of_females + person.gender.value

        # Now we must take the abs of num_of_males (because so far we have negative values, see Gender class for details)
        num_of_males = abs(num_of_males)
        return -1*abs(num_of_males - num_of_females)

    # The method below calculates non-normalized performance score based on big 5 trait

    def personality_performance(self) -> float:
        # First we take SD of each trait within the team
        # This lists RAW extraversion scores for all users within the team
        extrav_list = [
            user.personality.extraversion for user in self.userslist]
        # similarly we create other traits' lists below
        # For conscience
        conscience_list = [
            user.personality.conscience for user in self.userslist]
        openness_list = [user.personality.openness for user in self.userslist]
        agreeableness_list = [
            user.personality.agreeableness for user in self.userslist]
        neuroticism_list = [
            user.personality.neuroticism for user in self.userslist]

        # Now we take SD for each traits
        extrv_SD = st.stdev(extrav_list)
        conscience_SD = st.stdev(conscience_list)
        openness_SD = st.stdev(openness_list)
        agreeableness_SD = st.stdev(agreeableness_list)
        neuroticism_SD = st.stdev(neuroticism_list)

        # Now we take the average of all trait's SDs, which we argue to be RAW personality performance score for a team
        return (st.mean([extrv_SD, conscience_SD, openness_SD, agreeableness_SD, neuroticism_SD]))

    # Finally define the total performance (by adding the gender and personality performance)
    def total_team_performance(self) -> float:
        return (self.gender_performance() + self.personality_performance())

    # An additional method to help debugging
    def toString(self) -> str:
        temp = ""
        for i in range(0, len(self.userslist)):
            temp = temp + self.userslist[i].toString()+" "
        return temp
