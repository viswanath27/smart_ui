from typing import Any, Dict, Union
from react import useMemo, useReducer

# Extracts property names from initial state of reducer to allow typesafe dispatch objects
def FieldNames(T: Dict[str, Any]) -> Union[str, Dict[str, str]]:
    """
    Extracts property names from the initial state of the reducer to allow typesafe dispatch objects.

    Args:
        T: The initial state of the reducer.

    Returns:
        The property names.
    """
    return { K: K if isinstance(T[K], str) else K for K in T }

# Returns the Action Type for the dispatch object to be used for typing in things like context
def ActionType(T: Dict[str, Any]) -> Union[Dict[str, Any]]:
    """
    Returns the Action Type for the dispatch object to be used for typing in things like context.

    Args:
        T: The initial state of the reducer.

    Returns:
        The action type.
    """
    return Union[
        { 'type': 'reset' },
        { 'type': 'replace_all', 'value': T },
        { 'type': 'change', 'field': FieldNames(T), 'value': Any }
    ]

# Returns a typed dispatch and state
def useCreateReducer(initialState: Dict[str, Any]) -> Dict[str, Any]:
    """
    Custom hook for creating a reducer with typed dispatch and state.

    Args:
        initialState: The initial state of the reducer.

    Returns:
        A dictionary with the typed dispatch and state.
    """
    def reducer(state: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, Any]:
        if not action.get('type'):
            return { **state, action['field']: action['value'] }

        if action['type'] == 'replace_all':
            return action['value']
        if action['type'] == 'reset':
            return initialState

        raise Exception()

    state, dispatch = useReducer(reducer, initialState)

    return useMemo(lambda: { 'state': state, 'dispatch': dispatch }, [state, dispatch])
