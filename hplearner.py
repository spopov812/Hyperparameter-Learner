import pickle
import sys


'''

Class for HPLearner object which stores parameters then serializes them when hpsave() is called

'''


class HPLearner:

    # constructor
    def __init__(self):
        self.count = -1

        # tries to open dictionary that has experiment name as key and the value is another dicionary that links names
        # of params to their values
        try:
            self.exp_name_to_filename = pickle.load(open(".name_hpval", 'rb'))

        # first time running hplearner from this directory, file is created
        except FileNotFoundError or EOFError:
            with open(".name_hpval", 'wb') as f:
                pass

            # empty dictionary is created to begin storing experiment and value dictionary
            self.exp_name_to_filename = {}

        # premade params is created to support no name params if an experiment is not being loaded and run for the first
        # time
        self.experiment = ""
        self.params = {None: []}

        # checks for command line args if an experiment is to be loaded
        for i, arg in enumerate(sys.argv):

            if arg == "-hpload":
                self.experiment = sys.argv[i + 1]
                break

        # if loading experiment from file, load the hyperparameters
        if self.experiment != "":
            self.params = pickle.load(open(self.exp_name_to_filename[self.experiment], 'rb'))

    # increments counter that counts which no name arg will be returned next- used only if loading an experiment
    def increment(self):
        self.count += 1

    # overriding method that allows conveniant writing of the param name to param dictionary to a .p file
    def __repr__(self):

        string = ''

        # if hyperparameters with no name given were recorded
        if len(self.params[None]) != 0:
            string = "Unknown Parameters- \n"
            unkowns = [str(param) + "\n" for param in self.params[None]]

            # appends the unknown to string that will detail all the unknown params
            for unknown in unkowns:
                string += unknown

            string += '\n'

        # appends param name and param to return string
        for key in self.params.keys():
            if key is None:
                continue
            string += str(key) + "- "
            string += str(self.params[key]) + "\n"

        return string


# creates HPLearner object that is used to interact with necessary methods
hplearner = HPLearner()


# method that remembers hyperparams and their associated name
def hp(hyperparam, name=None):

    # not loading an experiment
    if hplearner.experiment == "":

        # no name given
        if name is None:
            # add this param to dictionary with a key of no name
            hplearner.params[None].append(hyperparam)
        else:
            # add this hyperparam to dictionary with appropriate name as a key
            hplearner.params[name] = hyperparam
        # the hyperparam that the user used is return as the same type
        return hyperparam

    # loaded an experiment
    else:

        # no name given
        if name is None:
            hplearner.increment()

            # return next hyperparameter with no name
            return hplearner.params[None][hplearner.count]
        # return hyperparameter with that name
        else:
            return hplearner.params[name]


# writing hyperparams to file and updating dictionary
def hpsave():

    # if an experiment was being loaded, no need to serialize it as a separate experiment
    if hplearner.experiment != "":
        return

    # sorts all experiments by name that have been serialized.
    # this is used to obtain the number of the last experiment
    experiment_filenames = list(hplearner.exp_name_to_filename.values())
    experiment_filenames.sort()

    experiment_number = ''

    # takes digit of the previous experiment and increments it
    try:
        
        for digit in experiment_filenames[-1][3:-2]:
        
            experiment_number += str(digit)

    # if this is the first experiment assign it as the first experiment
    except IndexError:

        experiment_number = 1


    experiment_number = int(experiment_number)

    # setting appropriate names for the experiment and filename
    exp_name = "Exp%d" % experiment_number
    exp_file_name = ".hp%d.p" % experiment_number

    # adds the name of the serialized file to dictionary that keeps track of experiments and their associated filenames
    hplearner.exp_name_to_filename[exp_name] = exp_file_name

    pickle.dump(hplearner.exp_name_to_filename, open(".name_hpval", 'wb'))
    pickle.dump(hplearner.params, open(exp_file_name, 'wb'))

    with open("hplog.txt", 'a') as f:

        f.write(exp_name + "-\n")
        f.writelines(hplearner.__repr__())
        f.write("\n\n")
