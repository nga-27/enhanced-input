from enhanced_input import EnhancedInput, EnhancedInputColor

def test():
    e_input = EnhancedInput()
    value = e_input.input("hello. Name? ", 20)
    print(value)
    value = e_input.input("ignore this... ", 3)
    print(value)
    value = e_input.input("Color me red! ", 3, text_color=EnhancedInputColor.RED)
    value = e_input.input("Color me cyan! ", 3, text_color=EnhancedInputColor.CYAN)
    value = e_input.input("Color me none... ", 3)
    print("done.")


if __name__ == "__main__":
    test()
