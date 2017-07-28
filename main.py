from entity import Entity
from component import TestComponent

def main():
    test = Entity([TestComponent], {"test": "testing..."})
    test.component_storage["test"].test(test)

if __name__ == "__main__":
    main()