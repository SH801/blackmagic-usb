

class Types:

    def getType(element):

        if type(element) == list:
            elementType = Types.getType(element[0])
            return {'isList': True, 'type': elementType['type']}
        else:
            try:
                elementType = element.__name__
            except AttributeError:
                elementType = type(element).__name__
            return {'isList': False, 'type': elementType}
