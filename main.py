from view.vue import View
from controller.controller import Controller


def main():
    object_view = View()
    object_controller: Controller = Controller(object_view)
    object_controller.start()


main()
