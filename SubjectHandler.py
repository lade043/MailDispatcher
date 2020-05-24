import re


class SubjectHandler:
    """
    class for managing all the sub-functions(nodes)
    """
    class Node:
        """
        node containing a sub-function
        """
        def __init__(self, regex, f):
            """
            creating node
            :param regex: regex checked against subject
            :param f: function to be called if keyword in subject
            """
            self.regex = regex
            self.func = f

    def __init__(self):
        self.nodes = []

    def __add__(self, other):
        """
        adding node to self
        :param other: node
        :return: self with added node
        """
        self.nodes.append(other)
        return self

    def __len__(self):
        return len(self.nodes)

    def run(self, messages):
        """
        running the class and checking if there's a regex match in any node and then running the node
        :param messages: array of messages, which should be checked
        :return: -
        """
        for message in messages:
            subject = message[0]
            for node in self.nodes:
                if re.match(node.regex, subject):
                    node.func(message)
