import os
import OID_view
import OID_model


class OID_controller:

    model = None
    view = None

    def __init__(self, model=OID_model, view=OID_view):
        self.model = model
        self.view = view

    def get_input_information(self):
        return self.model.get_input()


def main():
    model = OID_model.OID_model()
    controller = OID_controller(model, None)
    view = OID_view.OID_view(controller)
    controller.view = view
    view.start()


if __name__ == "__main__":
    main()
