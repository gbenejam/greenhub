'''
This script contains the command line interpreter class to be able to read command line options
passed to the greenGit.py script.
'''


USAGE = 'greenhub [options] [-c cron_expression]\n' \
'If you need to pass \'*\' as an argument to cron put it between quotes. \n' \
'Options:\n' \
'[-v] : verbose. Print all the commands that the program is executing to the standard output.\n' \
'[-h] : help. Print this usage string.\n' \
'[-n commits_number] : number of commits. Default is 1 commit per day.\n' \
'[-p path] : path of the project to be pushed. Default is \'.\'.\n' \
'Separate the options with spaces. The options that need extra parameters have to be followed by them.\n'


class CommandLineInterpreter():
    '''
    Class to create objects that represent the command line options. Each command line parameter
    is listed in the object as a separate parameter and the __str__ method returns the command
    entered to the command line.
    '''
    options = {'v': False, 'n': 1, 'p': '.', 'c': {}}
    
    cron_expression = '(crontab -l 2>/dev/null; echo "{0} {1} {2} {3} {4} {5} ' +\
        '-p {6} -n {7} -v >/tmp/greenhub.log 2>/tmp/greenhub_err.log") | crontab -'

    cron_parameters = ('minute', 'hour', 'month_day', 'month', 'week_day')

    def __init__(self, parameter_list):
        '''
        Initializes the object with the parameters passed as argument.
        parameter_list is the list of parameters received through the command line execution.
        Those optional parameters that are not specified in the list will be initialized with a
        default value if needed.
        '''
        # Variable to control if the program must end due to wrong parameters
        self.exit = False
        # First parameter is at position 1
        index = 1
        
        while index < len(parameter_list):
            arg = parameter_list[index]
            if arg[0] == '-':
                # option parameter
                if arg[1] in self.options:
                    index = self.__get_parameter_value__(arg[1], index + 1, parameter_list)
                elif arg[1] == 'h':
                    print(USAGE)
                    self.exit = True
                    return
                else:
                    print('Parameter not valid ({})'.format(arg))
                    print(USAGE)
                    raise Exception('Abort program')
            else:
                # We should not enter here, as the parameters without dash get read in the
                # __get_parameter_value__ method
                print('Error passing arguments ({})'.format(arg))
                print(USAGE)
                raise Exception('Abort program')
        
        # boolean to know if cron expression needs to be executed or not
        self.execute_cron = len(self.options['c']) > 0

    def __get_parameter_value__(self, arg_option, arg_value_index, parameter_list):
        '''
        This method fills the corresponding 'options' dictionary entry with the value
        read from the arguments passed to the script.
        It returns the index to the next parameter to be read from the parameter list.
        '''
        if arg_option == 'v':
            self.options['v'] = True
        elif arg_option == 'c':
            return self.__fill_cron_dict__(arg_value_index, parameter_list)
        elif arg_option == 'n':
            try:
                self.options['n'] = int(parameter_list[arg_value_index])
            except:
                print('Error parsing int')
                print(USAGE)
                raise Exception('Abort program')
            arg_value_index += 1
        elif arg_option == 'p':
            self.options['p'] = parameter_list[arg_value_index]
            arg_value_index += 1

        return arg_value_index

    def __fill_cron_dict__(self, arg_value_index, parameter_list):
        '''
        Fill the cron option in the dictionary with another dictionary with all the
        values for the crontab command. Default initialize those that are not set by
        the user to '*'.
        '''
        parameter = parameter_list[arg_value_index]
        index = 0
        
        while arg_value_index < len(parameter_list) and parameter[0] != '-':
            if index < len(self.cron_parameters):
                key = self.cron_parameters[index]
                value = parameter_list[arg_value_index]
                self.options['c'][key] = value
            else:
                # if there is still a parameter left and doesn't begin with '-' the __init__
                # method will detect and handle the error
                break
            
            # increment both indexes
            index += 1
            arg_value_index += 1

        # default initialize the rest of the cron expression with '*'
        while index < len(self.cron_parameters):
            key = self.cron_parameters[index]
            value = '*'
            self.options['c'][key] = value
            index += 1
        
        return arg_value_index
    
    def get_cron_expression(self, absolute_project_path, python_path):
        '''
        Getter for the cron expression entered as optional arguments.
        '''
        return CommandLineInterpreter.cron_expression.format(
            self.options['c'][self.cron_parameters[0]],
            self.options['c'][self.cron_parameters[1]],
            self.options['c'][self.cron_parameters[2]],
            self.options['c'][self.cron_parameters[3]],
            self.options['c'][self.cron_parameters[4]],
            python_path,
            absolute_project_path,
            self.get_commits_number())

    def get_project_path(self):
        '''
        Getter for the project path in where the script will execute its commands.
        '''
        return self.options['p']

    def get_commits_number(self):
        '''
        Getter for the number of commits to be pushed each day.
        '''
        return self.options['n']

    def is_verbose(self):
        '''
        Getter to check if the user marked the 'verbose' option or not.
        '''
        return self.options['v']


