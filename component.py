class TestComponent:
    name = "test"

    def __init__(self, options):
        """
        Test component.

        :param options: dict
        """
        self.component_storage["test"].string = options.get("test")

    def test(self):
        print(self.component_storage["test"].string)
