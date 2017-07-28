class Entity:
    def __init__(self, components, options):
        """
        Entity class.

        :param components: list<Component>
        :param options: dict
        """
        self.component_storage = {}
        for component in components:
            self.component_storage[component.name] = component
            self.component_storage[component.name].__init__(self, options)

    def has_component(self, component):
        """
        Returns True if entity has component.

        :param component: string/Component
        :return: bool
        """
        if type(component) == "string":
            return component in self.component_storage.keys()
        else:
            return component in self.component_storage
