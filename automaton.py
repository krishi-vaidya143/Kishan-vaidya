#!/usr/bin/env python3
# *-* coding=utf-8 *-*


class State():
    """
        Class for modeling a state in a finite state automaton.
    """
    def __init__(self, name):
        self.state = name
        self.successors = {}

    def set_successor(self, entry, successor):
        self.successors[entry] = successor

    def process(self, entry):
        """
            If no successor is defined, remain in current state
        """
        return self.successors.get(entry, self)

    def __repr__(self):
        return "State(state=%r)" % self.state


class Automaton():
    """
        Base class for Finite State Automata (FSA)
    """
    def __init__(self, states, init_state, input_alphabet, transition):
        """
            Creates a finite state automaton that only consists of
            - a set of states,
            - an initial state,
            - an input alphabet,
            - and a transition function.
            The transition is expected as a dictionary which maps
            pairs of elements to a successor state:
            (state, entry) -> successor
            transition[(state, entry)] == successor
        """
        self.states = {name: State(name) for name in states}
        self.input_alphabet = input_alphabet
        self.__curr_state = self.states[init_state]
        self.__connect_states(input_alphabet, transition)

    def process(self, entry):
        if entry not in self.input_alphabet:
            raise ValueError("Unspecified input, not accepted by this automaton!")
        self._exit_state(entry)
        self.__curr_state = self.__curr_state.process(entry)
        self._enter_state(entry)

    def __get_state(self):
        return self.__curr_state.state

    def __set_state(self, new_state):
        self.__curr_state = self.states[new_state]

    current_state = property(__get_state, __set_state)

    def __connect_states(self, input_alphabet, transition):
        for name, state in self.states.items():
            for entry in input_alphabet:
                if (name, entry) in transition:
                    successor_name = transition[(name, entry)]
                    successor = self.states[successor_name]
                    state.set_successor(entry, successor)

    def _enter_state(self, entry):
        pass

    def _exit_state(self, entry):
        pass

    def __repr__(self):
        return "Automaton(states={}, inputs={})".format(self.states.keys(),
                                                        self.input_alphabet)


class MooreAutomaton(Automaton):
    """
        A Moore automaton extends a primitive FSA by an output function, assigning
        an output to each state
    """
    def __init__(self, states, init_state, input_alphabet, transition, output_func):
        """
            This class expects in addition to the parameters of a simple FSA an
            output function. Unlike the transition 
        """
        Automaton.__init__(self, states, init_state, input_alphabet, transition)
        self.__output_func = output_func
        self._enter_state(None)

    def _enter_state(self, entry):
        self.__output_func(self.current_state)

class MealyAutomaton(Automaton):
    """
        A Moore automaton extends a primitive FSA by an output function, assigning
        an output to each state
    """
    def __init__(self, states, init_state, input_alphabet, transition, output_func):
        """
            This class expects in addition to the parameters of a simple FSA an
            output function. Unlike the transition 
        """
        Automaton.__init__(self, states, init_state, input_alphabet, transition)
        self.__output_func = output_func
        self._enter_state(None)

    def _exit_state(self, entry):
        self.__output_func(self.current_state, entry)
