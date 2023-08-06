"""
A simple toolkit for creating and simulating discrete stochastic models in
python.

"""
from __future__ import division
import ast
import signal, os
import numpy as np
import uuid
from contextlib import contextmanager
from collections import OrderedDict
from gillespy2.core.results import Trajectory,Results
from gillespy2.core.events import *
from gillespy2.core.gillespySolver import GillesPySolver
from gillespy2.core.gillespyError import *

try:
    import lxml.etree as eTree

    no_pretty_print = False

except:
    import xml.etree.ElementTree as eTree
    import xml.dom.minidom
    import re
    no_pretty_print = True

def import_SBML(filename, name=None, gillespy_model=None):
    """
    SBML to GillesPy model converter. NOTE: non-mass-action rates
    in terms of concentrations may not be converted for population
    simulation. Use caution when importing SBML.

    Attributes
    ----------
    filename : str
        Path to the SBML file for conversion.
    name : str
        Name of the resulting model.
    gillespy_model : gillespy.Model
        If desired, the SBML model may be added to an existing GillesPy model.
    """

    try:
        from gillespy2.sbml.SBMLimport import convert
    except ImportError:
        raise ImportError('SBML conversion not imported successfully')

    return convert(filename, model_name=name, gillespy_model=gillespy_model)


class SortableObject(object):
    """Base class for GillesPy2 objects that are sortable."""

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __lt__(self, other):
        return str(self) < str(other)

    def __le__(self, other):
        return str(self) <= str(other)

    def __cmp__(self, other):
        return cmp(str(self), str(other))

    def __hash__(self):
        if hasattr(self, '_hash'):
            return self._hash
        if hasattr(self, 'id'):
            self._hash = hash(self.id)
        elif hasattr(self, 'name'):
            self._hash = hash(self.name)
        else:
            self._hash = hash(self)
        return self._hash


class Model(SortableObject):
    # reserved names for model species/parameter names, volume, and operators.
    reserved_names = ['vol']
    special_characters = ['[', ']', '+', '-', '*', '/', '.', '^']

    """
    Representation of a well mixed biochemical model. Contains reactions,
    parameters, species.

    Attributes
    ----------
    name : str
        The name of the model, or an annotation describing it.
    population : bool
        The type of model being described. A discrete stochastic model is a
        population model (True), a deterministic model is a concentration model
        (False). Automatic conversion from population to concentration models
        may be used, by setting the volume parameter.
    volume : float
        The volume of the system matters when converting to from population to
        concentration form. This will also set a parameter "vol" for use in
        custom (i.e. non-mass-action) propensity functions.
    tspan : numpy ndarray
        The timepoints at which the model should be simulated. If None, a
        default timespan is added. May be set later, see Model.timespan
    annotation : str (optional)
        Optional further description of model
    """

    def __init__(self, name="", population=True, volume=1.0, tspan=None, annotation="model"):
        """ Create an empty model. """

        # The name that the model is referenced by (should be a String)
        self.name = name
        self.annotation = annotation

        # Dictionaries with model element objects.
        # Model element names are used as keys.
        self.listOfParameters = OrderedDict()
        self.listOfSpecies = OrderedDict()
        self.listOfReactions = OrderedDict()
        self.listOfAssignmentRules = OrderedDict()
        self.listOfRateRules = OrderedDict()
        self.listOfEvents = OrderedDict()
        self.listOfFunctionDefinitions = OrderedDict()

        # Dictionaries with model element objects.
        # Model element names are used as keys, and values are
        # sanitized versions of the names/formulas.
        # These dictionaries contain sanitized values and are for
        # Internal use only
        self._listOfParameters = OrderedDict()
        self._listOfSpecies = OrderedDict()
        self._listOfReactions = OrderedDict()
        self._listOfAssignmentRules = OrderedDict()
        self._listOfRateRules = OrderedDict()
        self._listOfEvents = OrderedDict()
        self._listOfFunctionDefinitions = OrderedDict()
        # This defines the unit system at work for all numbers in the model
        # It should be a logical error to leave this undefined, subclasses
        # should set it
        if population:
            self.units = "population"
        else:
            self.units = "concentration"
            if volume != 1.0:
                raise Warning(
                    "Concentration models account for volume implicitly, explicit volume definition is not required. "
                    "Note: concentration models may only be simulated deterministically.")

        self.volume = volume

        # Dict that holds flattended parameters and species for
        # evaluation of expressions in the scope of the model.
        self.namespace = OrderedDict([])

        if tspan is None:
            self.timespan(np.linspace(0, 20, 401))
        else:
            self.timespan(tspan)

    def __str__(self):
        divider = '\n**********\n'
        def decorate(header):
            return '\n' + divider + header + divider
        print_string = self.name
        if len(self.listOfSpecies):
            print_string += decorate('Species')
            for s in sorted(self.listOfSpecies.values()):
                print_string += '\n' + str(s)
        if len(self.listOfParameters):
            print_string += decorate('Parameters')
            for p in sorted(self.listOfParameters.values()):
                print_string += '\n' + str(p)
        if len(self.listOfReactions):
            print_string += decorate('Reactions')
            for r in sorted(self.listOfReactions.values()):
                print_string += '\n' + str(r)
        if len(self.listOfEvents):
            print_string += decorate('Events')
            for e in sorted(self.listOfEvents.values()):
                print_string += '\n' + str(e)
        if len(self.listOfAssignmentRules):
            print_string += decorate('Assignment Rules')
            for ar in sorted(self.listOfAssignmentRules.values()):
                print_string += '\n' + str(ar)
        if len(self.listOfRateRules):
            print_string += decorate('Rate Rules')
            for rr in sorted(self.listOfRateRules.values()):
                print_string += '\n' + str(rr)
        return print_string

    def serialize(self):
        """ Serializes the Model object to valid StochML. """
        self.resolve_parameters()
        doc = StochMLDocument().from_model(self)
        return doc.to_string()

    def update_namespace(self):
        """ Create a dict with flattened parameter and species objects. """
        self.namespace = OrderedDict([])
        for param in self.listOfParameters:
            self.namespace[param] = self.listOfParameters[param].value

    def sanitized_species_names(self):
        """
        Generate a dictionary mapping user chosen species names to simplified formats which will be used
        later on by GillesPySolvers evaluating reaction propensity functions.
        :return: the dictionary mapping user species names to their internal GillesPy notation.
        """
        species_name_mapping = OrderedDict([])
        for i, name in enumerate(sorted(self.listOfSpecies.keys())):
            species_name_mapping[name] = 'S[{}]'.format(i)
        return species_name_mapping

    def problem_with_name(self, name):
        if name in Model.reserved_names:
            return ModelError(
                'Name "{}" is unavailable. It is reserved for internal GillesPy use. Reserved Names: ({}).'.format(name,
                                                                                                                   Model.reserved_names))
        if name in self.listOfSpecies:
            return ModelError('Name "{}" is unavailable. A species with that name exists.'.format(name))
        if name in self.listOfParameters:
            return ModelError('Name "{}" is unavailable. A parameter with that name exists.'.format(name))
        if name.isdigit():
            return ModelError('Name "{}" is unavailable. Names must not be numeric strings.'.format(name))
        for special_character in Model.special_characters:
            if special_character in name:
                return ModelError(
                    'Name "{}" is unavailable. Names must not contain special characters: {}.'.format(name,
                                                                                                      Model.special_characters))

    def get_species(self, s_name):
        """
        Returns a species object by name.

        Attributes
        ----------
        s_name : str
            Name of the species object to be returned.
        """
        return self.listOfSpecies[s_name]

    def get_all_species(self):
        """
        Returns a dict of all species in the model, of the form:
        {name : species object}
        """
        return self.listOfSpecies

    def add_species(self, obj):
        """
        Adds a species, or list of species to the model.

        Attributes
        ----------
        obj : Species, or list of Species
            The species or list of species to be added to the model object.
        """
        if isinstance(obj, list):
            for S in sorted(obj):
                self.add_species(S)
        else:
            try:
                problem = self.problem_with_name(obj.name)
                if problem is not None:
                    raise problem
                self.listOfSpecies[obj.name] = obj
                self._listOfSpecies[obj.name] = 'S{}'.format(len(self._listOfSpecies))
            except Exception as e:
                raise ParameterError("Error using {} as a Species. Reason given: {}".format(obj, e))
        return obj

    def delete_species(self, obj):
        """
        Removes a species object by name.

        Attributes
        ----------
        obj : str
            Name of the species object to be removed.
        """
        self.listOfSpecies.pop(obj)
        self._listOfSpecies.pop(obj)

    def delete_all_species(self):
        """
        Removes all species from the model object.
        """
        self.listOfSpecies.clear()
        self._listOfSpecies.clear()

    def set_units(self, units):
        """
        Sets the units of the model to either "population" or "concentration"

        Attributes
        ----------
        units : str
            Either "population" or "concentration"
        """
        if units.lower() == 'concentration' or units.lower() == 'population':
            self.units = units.lower()
        else:
            raise ModelError("units must be either concentration or population (case insensitive)")

    def sanitized_parameter_names(self):
        """
        Generate a dictionary mapping user chosen parameter names to simplified formats which will be used
        later on by GillesPySolvers evaluating reaction propensity functions.
        :return: the dictionary mapping user parameter names to their internal GillesPy notation.
        """
        parameter_name_mapping = OrderedDict()
        parameter_name_mapping['vol'] = 'V'
        for i, name in enumerate(sorted(self.listOfParameters.keys())):
            if name not in parameter_name_mapping:
                parameter_name_mapping[name] = 'P{}'.format(i)
        return parameter_name_mapping

    def get_parameter(self, p_name):
        """
        Returns a parameter object by name.

        Attributes
        ----------
        p_name : str
            Name of the parameter object to be returned.
        """
        try:
            return self.listOfParameters[p_name]
        except:
            raise ModelError("No parameter named " + p_name)

    def get_all_parameters(self):
        """
        Returns a dict of all parameters in the model, of the form:
        {name : parameter object}
        """
        return self.listOfParameters

    def add_parameter(self, params):
        """

        Adds a parameter, or list of parameters to the model.

        Attributes
        ----------
        obj : Parameter, or list of Parameters
            The parameter or list of parameters to be added to the model object.
        """
        if isinstance(params, list):
            for p in sorted(params):
                self.add_parameter(p)
        else:
            try:
                problem = self.problem_with_name(params.name)
                if problem is not None:
                    raise problem
                self.listOfParameters[params.name] = params
                self._listOfParameters[params.name] = 'P{}'.format(len(self._listOfParameters))
            except Exception as e:
                raise ParameterError("Error using {} as a Parameter. Reason given: {}".format(params, e))
        return params

    def delete_parameter(self, obj):
        """
        Removes a parameter object by name.

        Attributes
        ----------
        obj : str
            Name of the parameter object to be removed.
        """
        self.listOfParameters.pop(obj)
        self._listOfParameters.pop(obj)

    def set_parameter(self, p_name, expression):
        """
        Set the value of an existing paramter "pname" to "expression".

        Attributes
        ----------
        p_name : str
            Name of the parameter whose value will be set.
        expression : str
            *String* that may be executed in C, describing the value of the
            parameter. May reference other parameters by name. (e.g. "k1*4")
        """

        p = self.listOfParameters[p_name]
        p.expression = expression
        p.evaluate()

    def resolve_parameters(self):
        """ Internal function:
        attempt to resolve all parameter expressions to scalar floats.
        This methods must be called before exporting the model. """
        self.update_namespace()
        for param in self.listOfParameters:
            try:
                self.listOfParameters[param].evaluate(self.namespace)
            except:
                raise ParameterError("Could not resolve Parameter expression {} to a scalar value.".format(param))

    def delete_all_parameters(self):
        """ Deletes all parameters from model. """
        self.listOfParameters.clear()
        self._listOfParameters.clear()

    def validate_reactants_and_products(self, reactions):
        for reactant in reactions.reactants.keys():
            if isinstance(reactant, str):
                if reactant not in self.listOfSpecies.keys():
                    raise ModelError(
                        'reactant: {0} for reaction {1} -- not found in model.listOfSpecies'.format(reactant,
                                                                                                    reactions.name))
                reactions.reactants[self.listOfSpecies[reactant]] = reactions.reactants[reactant]
                del reactions.reactants[reactant]
        for product in reactions.products.keys():
            if isinstance(product, str):
                if product not in self.listOfSpecies.keys():
                    raise ModelError('product: {0} for reaction {1} -- not found in model.listOfSpecies'.format(product,
                                                                                                                reactions.name))
                reactions.products[self.listOfSpecies[product]] = reactions.products[product]
                del reactions.products[product]

    def add_reaction(self, reactions):
        """
        Adds a reaction, or list of reactions to the model.

        Attributes
        ----------
        obj : Reaction, or list of Reactions
            The reaction or list of reaction objects to be added to the model
            object.
        """

        # TODO, make sure that you cannot overwrite an existing reaction
        if isinstance(reactions, list):
            for r in sorted(reactions):
                self.add_reaction(r)
        else:
            try:
                reactions.verify()
                self.validate_reactants_and_products(reactions)
                if reactions.name in self.listOfReactions:
                    raise ModelError("Duplicate name of reaction: {0}".format(reactions.name))
                self.listOfReactions[reactions.name] = reactions
                # Build Sanitized reaction as well
                sanitized_reaction = Reaction(name='R{}'.format(len(self._listOfReactions)))
                sanitized_reaction.reactants = {self._listOfSpecies[species.name]: reactions.reactants[species] for
                                                species in reactions.reactants}
                sanitized_reaction.products = {self._listOfSpecies[species.name]: reactions.products[species] for
                                               species in reactions.products}
                sanitized_reaction.propensity_function = reactions.sanitized_propensity_function(self._listOfSpecies,
                                                                                                 self._listOfParameters)
                self._listOfReactions[reactions.name] = sanitized_reaction
            except Exception as e:
                raise ParameterError("Error using {} as a Reaction. Reason given: {}".format(reactions, e))
        return reactions

    def add_rate_rule(self, rate_rules):
        """
                Adds a rate rule, or list of rate rules to the model.

                Attributes
                ----------
                obj : RateRule, or list of RateRules
                    The rate rule or list of rate rule objects to be added to the model
                    object.
                """

        if isinstance(rate_rules, list):
            for rr in sorted(rate_rules):
                self.add_rate_rule(rr)
        else:
            try:
                if len(self.listOfAssignmentRules) != 0:
                    for i in self.listOfAssignmentRules.values():
                        if rate_rules.variable == i.variable:
                            raise ModelError("Duplicate variable in rate_rules AND assignment_rules: {0}".
                                             format(rate_rules.variable))
                for i in self.listOfRateRules.values():
                    if rate_rules.variable == i.variable:
                        raise ModelError("Duplicate variable in rate_rules: {0}".format(rate_rules.variable))
                if rate_rules.name in self.listOfRateRules:
                    raise ModelError("Duplicate name of rate_rule: {0}".format(rate_rules.name))
                if rate_rules.formula == '':
                    raise ModelError('Invalid Rate Rule. Expression must be a non-empty string value')
                if rate_rules.variable == None:
                    raise ModelError('A GillesPy2 Rate Rule must be associated with a valid variable')

                self.listOfRateRules[rate_rules.name] = rate_rules
                sanitized_rate_rule = RateRule(name='RR{}'.format(len(self._listOfRateRules)))
                sanitized_rate_rule.formula = rate_rules.sanitized_formula(self._listOfSpecies,
                                                                           self._listOfParameters)
                self._listOfRateRules[rate_rules.name] = sanitized_rate_rule
            except Exception as e:
                raise ParameterError("Error using {} as a Rate Rule. Reason given: {}".format(rate_rules, e))
        return rate_rules

    def add_event(self, event):
        """
                Adds an event, or list of events to the model.

                Attributes
                ----------
                event : Event, or list of Events
                    The event or list of event objects to be added to the model
                    object.
                """

        if isinstance(event, list):
            for e in event:
                self.add_event(e)
        else:
            try:
                if event.trigger is None or not hasattr(event.trigger, 'expression'):
                    raise ModelError(
                        'An Event must contain a valid trigger.')
                for a in event.assignments:
                    if isinstance(a.variable, str):
                        if a.variable in self.listOfSpecies:
                            a.variable = self.listOfSpecies[a.variable]
                        else:
                            raise ModelError('{0} not a valid Species'.format(a.variable))
                self.listOfEvents[event.name] = event
            except Exception as e:
                raise ParameterError("Error using {} as Event. Reason given: {}".format(event, e))
        return event

    def add_function_definition(self, function_definitions):
        if isinstance(function_definitions, list):
            for fd in function_definitions:
                self.add_function_definition(fd)
        else:
            try:
                self.listOfFunctionDefinitions[function_definitions.name] = function_definitions
            except Exception as e:
                raise ParameterError(
                    "Error using {} as a Function Definition. Reason given: ".format(function_definitions, e))

    def add_assignment_rule(self, assignment_rules):
        if isinstance(assignment_rules, list):
            for ar in assignment_rules:
                self.add_assignment_rule(ar)
        else:
            try:
                if len(self.listOfRateRules) != 0:
                    for i in self.listOfRateRules.values():
                        if assignment_rules.variable == i.variable:
                            raise ModelError("Duplicate variable in rate_rules AND assignment_rules: {0}".
                                             format(assignment_rules.variable))
                for i in self.listOfAssignmentRules.values():
                    if assignment_rules.variable == i.variable:
                        raise ModelError("Duplicate variable in assignment_rules: {0}"
                                         .format(assignment_rules.variable))
                if assignment_rules.name in self.listOfAssignmentRules:
                    raise ModelError("Duplicate name in assignment_rules: {0}".format(assignment_rules.name))
                if assignment_rules.formula == '':
                    raise ModelError('Invalid Assignment Rule. Expression must be a non-empty string value')
                if assignment_rules.variable == None:
                    raise ModelError('A GillesPy2 Rate Rule must be associated with a valid variable')

                self.listOfAssignmentRules[assignment_rules.name] = assignment_rules
            except Exception as e:
                raise ParameterError("Error using {} as a Assignment Rule. Reason given: ".format(assignment_rules, e))

    def timespan(self, time_span):
        """
        Set the time span of simulation. StochKit does not support non-uniform
        timespans.

        tspan : numpy ndarray
            Evenly-spaced list of times at which to sample the species
            populations during the simulation.
        """

        items = np.diff(time_span)
        items = np.array([round(item, 10) for item in items])
        isuniform = (len(set(items)) == 1)

        if isuniform:
            self.tspan = time_span
        else:
            raise InvalidModelError("StochKit only supports uniform timespans")

    def get_reaction(self, rname):
        """

        :param rname: name of reaction to return
        :return: Reaction object
        """
        return self.listOfReactions[rname]

    def get_all_reactions(self):
        """
        :return: dict of all Reaction objects
        """
        return self.listOfReactions

    def delete_reaction(self, obj):
        """
        :param obj: Name of Reaction to be removed
        """
        self.listOfReactions.pop(obj)
        self._listOfReactions.pop(obj)

    def delete_all_reactions(self):
        """
        Clears all reactions in model
        """
        self.listOfReactions.clear()
        self._listOfReactions.clear()

    def get_event(self, ename):
        """
        :param ename: Name of Event to get
        :return: Event object
        """
        return self.listOfEvents[ename]

    def get_all_events(self):
        """
        :return: dict of all Event objects
        """
        return self.listOfEvents

    def delete_event(self, ename):
        """
        Removes specified Event from model
        :param ename: Name of Event to be removed
        """
        self.listOfEvents.pop(ename)
        self._listOfEvents.pop(ename)

    def delete_all_events(self):
        """
        Clears models events
        """
        self.listOfEvents.clear()
        self._listOfEvents.clear()

    def get_rate_rule(self, rname):
        """
        :param rname: Name of Rate Rule to get
        :return: RateRule object
        """
        return self.listOfRateRules[rname]

    def get_all_rate_rules(self):
        """
        :return: dict of all Rate Rule objects
        """
        return self.listOfRateRules

    def delete_rate_rule(self, rname):
        """
        Removes specified Rate Rule from model
        :param rname: Name of Rate Rule to be removed
        """
        self.listOfRateRules.pop(rname)
        self._listOfRateRules.pop(rname)

    def delete_all_rate_rules(self):
        """
        Clears all of models Rate Rules
        """
        self.listOfRateRules.clear()
        self._listOfRateRules.clear()

    def get_assignment_rule(self, aname):
        """
        :param aname: Name of Assignment Rule to get
        :return: Assignment Rule object
        """
        return self.listOfAssignmentRules[aname]

    def get_all_assignment_rules(self):
        """
        :return: dict of models Assignment Rules
        """
        return self.listOfAssignmentRules

    def delete_assignment_rule(self, aname):
        """
        Removes an assignment rule from a model
        :param aname: Name of AssignmentRule object to be removed from model
        """
        self.listOfAssignmentRules.pop(aname)
        self._listOfAssignmentRules.pop(aname)

    def delete_all_assignment_rules(self):
        """
        Clears all assignment rules from model
        """
        self.listOfAssignmentRules.clear()
        self._listOfAssignmentRules.clear()

    def get_function_definition(self, fname):
        """
        :param fname: name of Function to get
        :return: FunctionDefinition object
        """
        return self.listOfFunctionDefinitions[fname]

    def get_all_function_definitions(self):
        """
        :return: Dict of models function definitions
        """
        return self.listOfFunctionDefinitions

    def delete_function_definition(self, fname):
        """
        Removes specified Function Definition from model
        :param fname: Name of Function Definition to be removed
        """
        self.listOfFunctionDefinitions.pop(fname)
        self._listOfFunctionDefinitions.pop(fname)

    def delete_all_function_definitions(self):
        """
        Clears all Function Definitions from a model
        """
        self.listOfFunctionDefinitions.clear()
        self._listOfFunctionDefinitions.clear()

    def get_element(self, ename):
        """
        get element specified by name
        :param ename: name of element to search for
        :return:value of element, or 'element not found'
        """
        if ename in self.listOfReactions:
            return self.get_reaction(ename)
        if ename in self.listOfSpecies:
            return self.get_species(ename)
        if ename in self.listOfParameters:
            return self.get_parameter(ename)
        if ename in self.listOfEvents:
            return self.get_event(ename)
        if ename in self.listOfRateRules:
            return self.get_rate_rule(ename)
        if ename in self.listOfAssignmentRules:
            return self.get_assignment_rule(ename)
        if ename in self.listOfFunctionDefinitions:
            return self.get_function_definition(ename)
        return 'Element not found!'


    def get_best_solver(self, precompile=True):
        """
        Finds best solver for the users simulation. Currently, AssignmentRules, RateRules, FunctionDefinitions,
        Events, and Species with a dynamic, or continuous population must use the BasicTauHybridSolver.
        :param precompile: If True, and the model contains no AssignmentRules, RateRules, FunctionDefinitions, Events,
        or Species with a dynamic or continuous population, the get_best_solver will choose the VariableSSACSolver, else
        it will choose SSACSolver
        :type precompile: bool
        :return: gillespy2.gillespySolver
        """
        from gillespy2.solvers.numpy import can_use_numpy
        hybrid_check = False

        if len(self.get_all_assignment_rules()) or len(self.get_all_rate_rules())  \
                or len(self.get_all_function_definitions()) or len(self.get_all_events()):
            hybrid_check = True

        if len(self.get_all_species()) and hybrid_check == False:
            for i in self.get_all_species():
                tempMode = self.get_species(i).mode
                if tempMode == 'dynamic' or tempMode == 'continuous':
                    hybrid_check = True
                    break
        if can_use_numpy and hybrid_check:
            from gillespy2.solvers.numpy.basic_tau_hybrid_solver import BasicTauHybridSolver
            return BasicTauHybridSolver

        elif not can_use_numpy and hybrid_check:
            raise ModelError('BasicTauHybridSolver is the only solver currently that supports '
                             'AssignmentRules, RateRules, FunctionDefinitions, or Events. '
                             'Please install Numpy.')
        else:
            if precompile:
                from gillespy2.solvers.cpp.variable_ssa_c_solver import VariableSSACSolver
                return VariableSSACSolver
            from gillespy2.solvers.auto import SSASolver
            return SSASolver


    def run(self, solver=None, timeout=0, **solver_args):
        """
        Function calling simulation of the model. There are a number of
        parameters to be set here.

        Return
        ----------

        If show_labels is False, returns a numpy array of arrays of species population data. If show_labels is 
        True,returns a Results object that inherits UserList and contains one or more Trajectory objects that 
        inherit UserDict. Results object supports graphing and csv export.

        Attributes
        ----------
        solver : gillespy.GillesPySolver
            The solver by which to simulate the model. This solver object may
            be initialized separately to specify an algorithm. Optional, 
            defaults to ssa solver.
        timeout : int
            Allows a time_out value in seconds to be sent to a signal handler, restricting simulation run-time
        solver_args :
            solver-specific arguments to be passed to solver.run()
        """

        if solver is not None:
            try:
                solver_results, rc = solver.run(model=self, t=self.tspan[-1], increment=self.tspan[-1] - self.tspan[-2],
                                                timeout=timeout, **solver_args)
            except Exception as e:
                raise SimulationError(
                    "argument 'solver={}' to run() failed.  Reason Given: {}".format(solver, e))
        else:
            solver = self.get_best_solver()
            solver_results, rc = solver.run(model=self, t=self.tspan[-1], increment=self.tspan[-1] - self.tspan[-2],
                                            timeout=timeout, **solver_args)
        if rc == 33:
            from gillespy2.core import log
            log.warning('GillesPy2 simulation exceeded timeout.')

        if hasattr(solver_results[0], 'shape'):
            return solver_results

        if len(solver_results) == 1:
            results_list = [Trajectory(data=solver_results[0], model=self,
                                       solver_name=solver.name, rc=rc)]
            return Results(results_list)

        if len(solver_results) > 1:
            results_list = []
            for i in range(0, len(solver_results)):
                results_list.append(Trajectory(data=solver_results[i], model=self, solver_name=solver.name,
                                               rc=rc))
            return Results(results_list)

        else:
            raise ValueError("number_of_trajectories must be non-negative and non-zero")


class Species(SortableObject):
    """
    Chemical species. Can be added to Model object to interact with other
    species or time.

    Attributes
    ----------
    name : str
        The name by which this species will be called in reactions and within
        the model.
    initial_value : int >= 0
        Initial population of this species. If this is not provided as an int,
        the type will be changed when it is added by numpy.int
    constant: bool
        If true, the value of the species cannot be changed.
        (currently BasicTauHybridSolver only)
    boundary_condition: bool
        If true, species can be changed by events and rate rules, but not by
        reactions. (currently BasicTauHybridOnly)
    mode : str
        ***FOR USE WITH BasicTauHybridSolver ONLY***
        Sets the mode of representation of this species for the TauHybridSolver,
        can be discrete, continuous, or dynamic.
        mode='dynamic' - Allows a species to be represented as
            either discrete or continuous
        mode='continuous' - Species will only be represented as continuous
        mode='discrete' - Species will only be represented as discrete
    allow_negative_populations: bool
        If true, population can be reduced below 0
    switch_tol : float
        ***FOR USE WITH BasicTauHybridSolver ONLY***
        Tolerance level for considering a dynamic species deterministically,
        value is compared to an estimated sd/mean population of a species after a
        given time step. This value will be used if a switch_min is not
        provided.  The default value is 0.03
    switch_min : float
        ***FOR USE WITH BasicTauHybridSolver ONLY***
        Minimum population value at which species will be represented as
        continuous. If a value is given, switch_min will be used instead of
        switch_tol
        
    """

    def __init__(self, name="", initial_value=0, constant=False,
                 boundary_condition=False, mode=None,
                 allow_negative_populations=False, switch_min=0,
                 switch_tol=0.03):
        # A species has a name (string) and an initial value (positive integer)
        self.name = name
        self.constant = constant
        self.boundary_condition = boundary_condition
        self.mode = mode
        self.allow_negative_populations = allow_negative_populations
        self.switch_min = switch_min
        self.switch_tol = switch_tol

        mode_list = ['continuous', 'dynamic', 'discrete',None]

        if self.mode not in mode_list:
            raise SpeciesError('Species mode must be either \'continuous\', \'dynamic\', \'discrete\', or '
                               '\'unspecified(default to dynamic for BasicTauHybridSolver)\'.')
        if mode == 'continuous':
            self.initial_value = np.float(initial_value)
        else:
            if np.int(initial_value) != initial_value:
                raise ValueError(
                    "'initial_value' for Species with mode='discrete' must be an integer value. Change to mode='continuous' to use floating point values.")
            self.initial_value = np.int(initial_value)
        if not allow_negative_populations:
            if self.initial_value < 0: raise ValueError('A species initial value must be \
non-negative unless allow_negative_populations=True')

    def __str__(self):
        print_string = self.name
        print_string += ': ' + str(self.initial_value)
        '''
        print_string += '\n\tInitial Value: ' + str(self.initial_value)
        print_string += '\n\tConstant: ' + str(self.constant)
        print_string += '\n\tBoundary Condition: ' + str(self.boundary_condition)
        print_string += '\n\tMode: ' + self.mode
        print_string += '\n\tAllow Negative Populations: ' + str(self.allow_negative_populations)
        '''
        return print_string

    def set_initial_value(self, num):
        """
        Setter method for initial_value of a population
        :param num: Integer to set initial species population
        :raises SpeciesError: If num is non-negative or a decimal number
        """
        print(num)
        print(self.mode)
        if isinstance(num, float) and (self.mode != 'dynamic' or self.mode != 'continuous'):
            raise SpeciesError("Mode set to discrete, species must be an integer number.")
        if num < 0 and self.allow_negative_populations == False:
            raise SpeciesError("Species population must be non-negative, or allow_negative_populations "
                               "must be set to True")
        self.initial_value = num


class Parameter(SortableObject):
    """
    A parameter can be given as an expression (function) or directly
    as a value (scalar). If given an expression, it should be
    understood as evaluable in the namespace of a parent Model.

    Attributes
    ----------
    name : str
        The name by which this parameter is called or referenced in reactions.
    expression : str
        String for a function calculating parameter values. Should be evaluable
        in namespace of Model.
    value : float
        Value of a parameter if it is not dependent on other Model entities.
    """

    def __init__(self, name="", expression=None, value=None):

        self.name = name
        # We allow expression to be passed in as a non-string type. Invalid strings
        # will be caught below. It is perfectly fine to give a scalar value as the expression.
        # This can then be evaluated in an empty namespace to the scalar value.
        self.expression = expression
        if expression is not None:
            self.expression = str(expression)

        self.value = value

        # self.value is allowed to be None, but not self.expression. self.value
        # might not be evaluable in the namespace of this parameter, but defined
        # in the context of a model or reaction.
        if self.expression is None:
            raise TypeError

        if self.value is None:
            self.evaluate()

    def __str__(self):
        return self.name + ': ' + self.expression

    def evaluate(self, namespace={}):
        """
        Evaluate the expression and return the (scalar) value in the given
        namespace.

        Attributes
        ----------
        namespace : dict (optional)
            The namespace in which to test evaluation of the parameter, if it
            involves other parameters, etc.
        """
        try:
            self.value = (float(eval(self.expression, namespace)))
        except:
            self.value = None

    def set_expression(self, expression):
        """
        Sets the expression for a parameter.
        """
        self.expression = expression
        # We allow expression to be passed in as a non-string type. Invalid
        # strings will be caught below. It is perfectly fine to give a scalar
        # value as the expression. This can then be evaluated in an empty
        # namespace to the scalar value.
        if expression is not None:
            self.expression = str(expression)

        if self.expression is None:
            raise TypeError

        self.evaluate()


class FunctionDefinition(SortableObject):
    """
    Object representation defining an evaluable function to be used during
    simulation of a GillesPy2 model

    Attributes
    ----------
    name : str
        Name of the function to be made and called.
    function : str
        Defined function body of operation to be performed.
    variables : list
        String names of Variables to be used as arguments to function.
    """


    def __init__(self, name="", function=None, args=[]):

        import math
        eval_globals = math.__dict__

        self.name = name
        args = ', '.join(args)
        self.function = eval('lambda ' + args + ': ' + function, eval_globals)
        if self.function is None:
            raise TypeError

    def sanitized_function(self, species_mappings, parameter_mappings):
        names = sorted(list(species_mappings.keys()) + list(parameter_mappings.keys()), key=lambda x: len(x),
                       reverse=True)
        replacements = [parameter_mappings[name] if name in parameter_mappings else species_mappings[name]
                        for name in names]
        sanitized_function = self.function
        for id, name in enumerate(names):
            sanitized_function = sanitized_function.replace(name, "{" + str(id) + "}")
        return sanitized_function.format(*replacements)


class AssignmentRule(SortableObject):
    """
    An AssignmentRule is used to express equations that set the values of
    variables.  This would correspond to a function in the form of x = f(V)

    Attributes
    ----------
    name : str
        Name of the Rule
    variable : str
        Target Species/Parameter to be modified by rule
    formula : str
        String representation of formula to be evaluated
    """

    def __init__(self, variable=None, formula=None, name=None):
        self.variable = variable
        self.formula = formula
        self.name = name

    def __str__(self):
        return self.variable + ': ' + self.formula

    def sanitized_formula(self, species_mappings, parameter_mappings):
        names = sorted(list(species_mappings.keys()) + list(parameter_mappings.keys()), key=lambda x: len(x),
                       reverse=True)
        replacements = [parameter_mappings[name] if name in parameter_mappings else species_mappings[name]
                        for name in names]
        sanitized_formula = self.formula
        for id, name in enumerate(names):
            sanitized_formula = sanitized_formula.replace(name, "{" + str(id) + "}")
        return sanitized_formula.format(*replacements)


class RateRule(SortableObject):
    """
    A RateRule is used to express equations that determine the rates of change
    of variables. This would correspond to a function in the form of dx/dt=f(W)

    Attributes
    ----------
    name : str
        Name of Rule
    variable : str
        Target Species/Parameter to be modified by rule
    formula : str
        String representation of formula to be evaluated
    """

    def __init__(self, variable=None, formula='', name=None):
        self.formula = formula
        self.variable = variable
        self.name = name

    def __str__(self):
        try:
            return self.name + ': Var: ' + self.variable + ': ' + self.formula
        except:
            return 'Rate Rule: {} contains an invalid variable or formula'.format(self.name)

    def sanitized_formula(self, species_mappings, parameter_mappings):
        names = sorted(list(species_mappings.keys()) + list(parameter_mappings.keys()), key=lambda x: len(x),
                       reverse=True)
        replacements = [parameter_mappings[name] if name in parameter_mappings else species_mappings[name]
                        for name in names]
        sanitized_formula = self.formula
        for id, name in enumerate(names):
            sanitized_formula = sanitized_formula.replace(name, "{" + str(id) + "}")
        return sanitized_formula.format(*replacements)


class Reaction(SortableObject):
    """
    Models a single reaction. A reaction has its own dicts of species
    (reactants and products) and parameters. The reaction's propensity
    function needs to be evaluable (and result in a non-negative scalar
    value) in the namespace defined by the union of those dicts.

    Attributes
    ----------
    name : str
        The name by which the reaction is called (optional).
    reactants : dict
        The reactants that are consumed in the reaction, with stoichiometry. An
        example would be {R1 : 1, R2 : 2} if the reaction consumes two of R1 and
        one of R2, where R1 and R2 are Species objects.
    products : dict
        The species that are created by the reaction event, with stoichiometry.
        Same format as reactants.
    propensity_function : str
        The custom propensity fcn for the reaction. Must be evaluable in the
        namespace of the reaction using C operations.
    massaction : bool
        The switch to use a mass-action reaction. If set to True, a rate value
        is required.
    rate : float
        The rate of the mass-action reaction. Take care to note the units...
    annotation : str
        An optional note about the reaction.

    Notes
    ----------
    For a species that is NOT consumed in the reaction but is part of a mass
    action reaction, add it as both a reactant and a product.

    Mass-action reactions must also have a rate term added. Note that the input
    rate represents the mass-action constant rate independent of volume.
    """

    def __init__(self, name="", reactants={}, products={},
                 propensity_function=None, massaction=False,
                 rate=None, annotation=None):
        """
        Initializes the reaction using short-hand notation.
        """

        # Metadata
        if name == "" or name is None:
            self.name = 'rxn' + str(uuid.uuid4()).replace('-', '_')
        else:
            self.name = name
        self.annotation = ""

        # We might use this flag in the future to automatically generate
        # the propensity function if set to True.
        if propensity_function is not None:
            self.massaction = False
            self.marate = None
        else:
            self.massaction = True

        self.propensity_function = propensity_function
        self.ode_propensity_function = propensity_function

        if self.propensity_function is not None and self.massaction:
            errmsg = ("Reaction {} You cannot set the propensity type to mass-action and simultaneously set a "
                      "propensity function.").format(self.name)
            raise ReactionError(errmsg)

        self.reactants = {}
        for r in reactants:
            rtype = type(r).__name__
            if rtype == 'instance':
                self.reactants[r.name] = reactants[r]
            else:
                self.reactants[r] = reactants[r]

        self.products = {}
        for p in products:
            rtype = type(p).__name__
            if rtype == 'instance':
                self.products[p.name] = products[p]
            else:
                self.products[p] = products[p]

        if self.massaction:
            self.type = "mass-action"
            if rate is None:
                self.marate = None
            else:
                self.marate = rate
                self.__create_mass_action()
        else:
            self.type = "customized"

            def __customPropParser():
                pow_func = ast.parse("pow", mode="eval").body

                class ExpressionParser(ast.NodeTransformer):
                    def visit_BinOp(self, node):
                        node.left = self.visit(node.left)
                        node.right = self.visit(node.right)
                        if isinstance(node.op, (ast.BitXor, ast.Pow)):
                            # ast.Call calls defined function, args include which nodes
                            # are effected by function call
                            call = ast.Call(func=pow_func,
                                            args=[node.left, node.right],
                                            keywords=[])
                            # Copy_location copies lineno and coloffset attributes
                            # from old node to new node. ast.copy_location(new_node,old_node)
                            call = ast.copy_location(call, node)
                            # Return changed node
                            return call
                        # No modification to node, classes extending NodeTransformer methods
                        # Always return node or value
                        else:
                            return node

                    def visit_Name(self, node):
                        #Visits Name nodes, if the name nodes "id" value is 'e', replace with numerical constant
                        if node.id == 'e':
                            nameToConstant = ast.copy_location(ast.Num(float(np.e), ctx=node.ctx), node)
                            return nameToConstant
                        return node

                expr = self.propensity_function
                expr = expr.replace('^', '**')
                expr = ast.parse(expr, mode='eval')
                expr = ExpressionParser().visit(expr)

                class ToString(ast.NodeVisitor):
                    def __init__(self):
                        self.string = ''
                    def _string_changer(self, addition):
                        self.string += addition
                    def visit_BinOp(self, node):
                        self._string_changer('(')
                        self.visit(node.left)
                        self.visit(node.op)
                        self.visit(node.right)
                        self._string_changer(')')
                    def visit_Name(self, node):
                        self._string_changer(node.id)
                        self.generic_visit(node)
                    def visit_Num(self, node):
                        self._string_changer(str(node.n))
                        self.generic_visit(node)
                    def visit_Call(self, node):
                        self._string_changer(node.func.id + '(')
                        counter = 0
                        for arg in node.args:
                            self.visit(arg)
                            if counter == 0:
                                self._string_changer(',')
                                counter += 1
                        self._string_changer(')')
                    def visit_Add(self, node):
                        self._string_changer('+')
                        self.generic_visit(node)
                    def visit_Div(self, node):
                        self._string_changer('/')
                        self.generic_visit(node)
                    def visit_Mult(self, node):
                        self._string_changer('*')
                        self.generic_visit(node)
                    def visit_UnaryOp(self, node):
                        self._string_changer('(')
                        self.visit_Usub(node)
                        self._string_changer(')')
                    def visit_Sub(self, node):
                        self._string_changer('-')
                        self.generic_visit(node)
                    def visit_Usub(self, node):
                        self._string_changer('-')
                        self.generic_visit(node)

                newFunc = ToString()
                newFunc.visit(expr)
                return newFunc.string

            self.propensity_function = __customPropParser()

    def __str__(self):
        print_string = self.name
        if len(self.reactants):
            print_string += '\n\tReactants'
            for r, stoich in self.reactants.items():
                try:
                    print_string += '\n\t\t' + r.name + ': ' + str(stoich)
                except Exception as e:
                    print_string += '\n\t\t' + r + ': ' + 'INVALID - ' + str(e)
        if len(self.products):
            print_string += '\n\tProducts'
            for p, stoich in self.products.items():
                try:
                    print_string += '\n\t\t' + p.name + ': ' + str(stoich)
                except Exception as e:
                    print_string += '\n\t\t' + p + ': ' + 'INVALID - ' + str(e)
        print_string += '\n\tPropensity Function: ' + self.propensity_function
        return print_string

    def verify(self):
        """ Check if the reaction is properly formatted.
        Does nothing on sucesss, raises and error on failure."""
        if self.marate is None and self.propensity_function is None:
            raise ReactionError("You must specify either a mass-action rate or a propensity function")
        if len(self.reactants) == 0 and len(self.products) == 0:
            raise ReactionError("You must have a non-zero number of reactants or products.")

    def __create_mass_action(self):
        """
        Initializes the mass action propensity function given
        self.reactants and a single parameter value.
        """
        # We support zeroth, first and second order propensities only.
        # There is no theoretical justification for higher order propensities.
        # Users can still create such propensities if they really want to,
        # but should then use a custom propensity.
        total_stoch = 0
        for r in sorted(self.reactants):
            total_stoch += self.reactants[r]
        if total_stoch > 2:
            raise ReactionError("Reaction: A mass-action reaction cannot involve more than two of one species or one "
                                "of two species. To declare a custom propensity, replace 'rate' with "
                                "'propensity_function'.")

        # Case EmptySet -> Y

        propensity_function = self.marate.name
        ode_propensity_function = self.marate.name

        # There are only three ways to get 'total_stoch==2':
        for r in sorted(self.reactants):
            if isinstance(r, str):
                rname = r
            else:
                rname = r.name
            # Case 1: 2X -> Y
            if self.reactants[r] == 2:
                propensity_function = (propensity_function +
                                       "*" + rname + "*(" + rname + "-1)/vol")
                ode_propensity_function += '*' + rname + '*' + rname
            else:
                # Case 3: X1, X2 -> Y;
                propensity_function += "*" + rname
                ode_propensity_function += '*' + rname

        # Set the volume dependency based on order.
        order = len(self.reactants)
        if order == 2:
            propensity_function += "/vol"
        elif order == 0:
            propensity_function += "*vol"

        self.propensity_function = propensity_function
        self.ode_propensity_function = ode_propensity_function

    def setType(self, rxntype):
        """
        Sets reaction type to either "mass-action" or "customized"

        Attributes
        ----------
        rxntype : str
            Either "mass-action" or "customized"
        """
        if rxntype.lower() not in {'mass-action', 'customized'}:
            raise ReactionError("Invalid reaction type.")
        self.type = rxntype.lower()

        self.massaction = False if self.type == 'customized' else True

    def addReactant(self, S, stoichiometry):
        """
        Adds a reactant to the reaction (species that is consumed)

        Attributes
        ----------
        S : gillespy.Species
            Reactant to add to this reaction.
        stoichiometry : int
            The stoichiometry of the given reactant.
        """
        if stoichiometry <= 0:
            raise ReactionError("Reaction Stoichiometry must be a \
                                    positive integer.")
        self.reactants[S.name] = stoichiometry

    def addProduct(self, S, stoichiometry):
        """
        Adds a product to the reaction (species that is created)

        Attributes
        ----------
        S : gillespy.Species
            Product to add to this reaction.
        stoichiometry : int
            The stoichiometry of the given product.
        """
        self.products[S.name] = stoichiometry

    def Annotate(self, annotation):
        """
        Adds a note to the reaction

        Attributes
        ----------
        annotation : str
            An optional note about the reaction.
        """
        self.annotation = annotation

    def sanitized_propensity_function(self, species_mappings, parameter_mappings):
        names = sorted(list(species_mappings.keys()) + list(parameter_mappings.keys()), key=lambda x: len(x),
                       reverse=True)
        replacements = [parameter_mappings[name] if name in parameter_mappings else species_mappings[name]
                        for name in names]
        sanitized_propensity = self.propensity_function
        for id, name in enumerate(names):
            sanitized_propensity = sanitized_propensity.replace(name, "{" + str(id) + "}")
        return sanitized_propensity.format(*replacements)


class StochMLDocument():
    """ Serializiation and deserialization of a Model to/from
        the native StochKit2 XML format. """

    def __init__(self):
        # The root element
        self.document = eTree.Element("Model")
        self.annotation = None

    @classmethod
    def from_model(cls, model):
        """
        Creates an StochKit XML document from an exisiting Mdoel object.
        This method assumes that all the parameters in the model are already
        resolved to scalar floats (see Model.resolveParamters).

        Note, this method is intended to be used interanally by the models
        'serialization' function, which performs additional operations and
        tests on the model prior to writing out the XML file. You should NOT \
        do:

        document = StochMLDocument.fromModel(model)
        print document.toString()

        You SHOULD do

        print model.serialize()

        """

        # Description
        md = cls()

        d = eTree.Element('Description')

        #
        if model.units.lower() == "concentration":
            d.set('units', model.units.lower())

        d.text = model.annotation
        md.document.append(d)

        # Number of Reactions
        nr = eTree.Element('NumberOfReactions')
        nr.text = str(len(model.listOfReactions))
        md.document.append(nr)

        # Number of Species
        ns = eTree.Element('NumberOfSpecies')
        ns.text = str(len(model.listOfSpecies))
        md.document.append(ns)

        # Species
        spec = eTree.Element('SpeciesList')
        for sname in model.listOfSpecies:
            spec.append(md.__species_to_element(model.listOfSpecies[sname]))
        md.document.append(spec)

        # Parameters
        params = eTree.Element('ParametersList')
        for pname in model.listOfParameters:
            params.append(md.__parameter_to_element(
                model.listOfParameters[pname]))

        params.append(md.__parameter_to_element(Parameter(name='vol', expression=model.volume)))

        md.document.append(params)

        # Reactions
        reacs = eTree.Element('ReactionsList')
        for rname in model.listOfReactions:
            reacs.append(md.__reaction_to_element(model.listOfReactions[rname], model.volume))
        md.document.append(reacs)

        return md

    @classmethod
    def from_file(cls, filepath):
        """ Intializes the document from an exisiting native StochKit XML
        file read from disk. """
        tree = eTree.parse(filepath)
        root = tree.getroot()
        md = cls()
        md.document = root
        return md

    @classmethod
    def from_string(cls, string):
        """ Intializes the document from an exisiting native StochKit XML
        file read from disk. """
        root = eTree.fromString(string)

        md = cls()
        md.document = root
        return md

    def to_model(self, name):
        """ Instantiates a Model object from a StochMLDocument. """

        # Empty model
        model = Model(name=name)
        root = self.document

        # Try to set name from document
        if model.name == "":
            name = root.find('Name')
            if name.text is None:
                raise NameError("The Name cannot be none")
            else:
                model.name = name.text

        # Set annotiation
        ann = root.find('Description')
        if ann is not None:
            units = ann.get('units')

            if units:
                units = units.strip().lower()

            if units == "concentration":
                model.units = "concentration"
            elif units == "population":
                model.units = "population"
            else:  # Default
                model.units = "population"

            if ann.text is None:
                model.annotation = ""
            else:
                model.annotation = ann.text

        # Set units
        units = root.find('Units')
        if units is not None:
            if units.text.strip().lower() == "concentration":
                model.units = "concentration"
            elif units.text.strip().lower() == "population":
                model.units = "population"
            else:  # Default
                model.units = "population"

        # Create parameters
        for px in root.iter('Parameter'):
            name = px.find('Id').text
            expr = px.find('Expression').text
            if name.lower() == 'vol' or name.lower() == 'volume':
                model.volume = float(expr)
            else:
                p = Parameter(name, expression=expr)
                # Try to evaluate the expression in the empty namespace
                # (if the expr is a scalar value)
                p.evaluate()
                model.add_parameter(p)

        # Create species
        for spec in root.iter('Species'):
            name = spec.find('Id').text
            val = spec.find('InitialPopulation').text
            if '.' in val:
                val = float(val)
            else:
                val = int(val)
            s = Species(name, initial_value=val)
            model.add_species([s])

        # The namespace_propensity for evaluating the propensity function
        # for reactions must contain all the species and parameters.
        namespace_propensity = OrderedDict()
        all_species = model.get_all_species()
        all_parameters = model.get_all_parameters()

        for param in all_species:
            namespace_propensity[param] = all_species[param].initial_value

        for param in all_parameters:
            namespace_propensity[param] = all_parameters[param].value

        # Create reactions
        for reac in root.iter('Reaction'):
            try:
                name = reac.find('Id').text
            except:
                raise InvalidStochMLError("Reaction has no name.")

            reaction = Reaction(name=name, reactants={}, products={})

            # Type may be 'mass-action','customized'
            try:
                type = reac.find('Type').text
            except:
                raise InvalidStochMLError("No reaction type specified.")

            reactants = reac.find('Reactants')
            try:
                for ss in reactants.iter('SpeciesReference'):
                    specname = ss.get('id')
                    # The stochiometry should be an integer value, but some
                    # exising StoxhKit models have them as floats. This is
                    # why we need the slightly odd conversion below.
                    stoch = int(float(ss.get('stoichiometry')))
                    # Select a reference to species with name specname
                    sref = model.listOfSpecies[specname]
                    try:
                        # The sref list should only contain one element if
                        # the XML file is valid.
                        reaction.reactants[sref] = stoch
                    except Exception as e:
                        StochMLImportError(e)
            except:
                # Yes, this is correct. 'reactants' can be None
                pass

            products = reac.find('Products')
            try:
                for ss in products.iter('SpeciesReference'):
                    specname = ss.get('id')
                    stoch = int(float(ss.get('stoichiometry')))
                    sref = model.listOfSpecies[specname]
                    try:
                        # The sref list should only contain one element if
                        # the XML file is valid.
                        reaction.products[sref] = stoch
                    except Exception as e:
                        raise StochMLImportError(e)
            except:
                # Yes, this is correct. 'products' can be None
                pass

            if type == 'mass-action':
                reaction.massaction = True
                reaction.type = 'mass-action'
                # If it is mass-action, a parameter reference is needed.
                # This has to be a reference to a species instance. We
                # explicitly disallow a scalar value to be passed as the
                # parameter.
                try:
                    ratename = reac.find('Rate').text
                    try:
                        reaction.marate = model.listOfParameters[ratename]
                    except KeyError as k:
                        # No paramter name is given. This is a valid use case
                        # in StochKit. We generate a name for the paramter,
                        # and create a new parameter instance. The parameter's
                        # value should now be found in 'ratename'.
                        generated_rate_name = "Reaction_" + name + \
                                              "_rate_constant"
                        p = Parameter(name=generated_rate_name,
                                      expression=ratename)
                        # Try to evaluate the parameter to set its value
                        p.evaluate()
                        model.add_parameter(p)
                        reaction.marate = model.listOfParameters[
                            generated_rate_name]

                    reaction.__create_mass_action()
                except Exception as e:
                    raise
            elif type == 'customized':
                try:
                    propfunc = reac.find('PropensityFunction').text
                except Exception as e:
                    raise InvalidStochMLError(
                        "Found a customized propensity function, but no expression was given. {}".format(e))
                reaction.propensity_function = propfunc
            else:
                raise InvalidStochMLError(
                    "Unsupported or no reaction type given for reaction" + name)

            model.add_reaction(reaction)

        return model

    def to_string(self):
        """ Returns  the document as a string. """
        try:
            doc = eTree.tostring(self.document, pretty_print=True)
            return doc.decode("utf-8")
        except:
            # Hack to print pretty xml without pretty-print
            # (requires the lxml module).
            doc = eTree.tostring(self.document)
            xmldoc = xml.dom.minidom.parseString(doc)
            uglyXml = xmldoc.toprettyxml(indent='  ')
            text_re = re.compile(">\n\s+([^<>\s].*?)\n\s+</", re.DOTALL)
            prettyXml = text_re.sub(">\g<1></", uglyXml)
            return prettyXml

    def __species_to_element(self, S):
        e = eTree.Element('Species')
        idElement = eTree.Element('Id')
        idElement.text = S.name
        e.append(idElement)

        if hasattr(S, 'description'):
            descriptionElement = eTree.Element('Description')
            descriptionElement.text = S.description
            e.append(descriptionElement)

        initialPopulationElement = eTree.Element('InitialPopulation')
        initialPopulationElement.text = str(S.initial_value)
        e.append(initialPopulationElement)

        return e

    def __parameter_to_element(self, P):
        e = eTree.Element('Parameter')
        idElement = eTree.Element('Id')
        idElement.text = P.name
        e.append(idElement)
        expressionElement = eTree.Element('Expression')
        expressionElement.text = str(P.value)
        e.append(expressionElement)
        return e

    def __reaction_to_element(self, R, model_volume):
        e = eTree.Element('Reaction')

        idElement = eTree.Element('Id')
        idElement.text = R.name
        e.append(idElement)

        descriptionElement = eTree.Element('Description')
        descriptionElement.text = self.annotation
        e.append(descriptionElement)

        # StochKit2 wants a rate for mass-action propensites
        if R.massaction and model_volume == 1.0:
            rateElement = eTree.Element('Rate')
            # A mass-action reactions should only have one parameter
            rateElement.text = R.marate.name
            typeElement = eTree.Element('Type')
            typeElement.text = 'mass-action'
            e.append(typeElement)
            e.append(rateElement)

        else:
            typeElement = eTree.Element('Type')
            typeElement.text = 'customized'
            e.append(typeElement)
            functionElement = eTree.Element('PropensityFunction')
            functionElement.text = R.propensity_function
            e.append(functionElement)

        reactants = eTree.Element('Reactants')

        for reactant, stoichiometry in R.reactants.items():
            srElement = eTree.Element('SpeciesReference')
            srElement.set('id', str(reactant))
            srElement.set('stoichiometry', str(stoichiometry))
            reactants.append(srElement)

        e.append(reactants)

        products = eTree.Element('Products')
        for product, stoichiometry in R.products.items():
            srElement = eTree.Element('SpeciesReference')
            srElement.set('id', str(product))
            srElement.set('stoichiometry', str(stoichiometry))
            products.append(srElement)
        e.append(products)

        return e
