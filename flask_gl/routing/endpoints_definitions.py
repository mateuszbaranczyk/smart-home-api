def create_definitions(devices: list[str]) -> str:
    functions = ["on-off", "set-timer", "set-warm", "set-color"]
    definitions = "- all, All\n" + "".join(
        f"-- {device.lower()},{device.capitalize()}\n"
        + "".join(  # noqa
            f"--- {device}_{func},{func},/{func.lower()}/{device.lower()}\n"
            for func in functions
        )
        for device in devices
    )
    return definitions
