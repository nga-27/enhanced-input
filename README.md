# enhanced-input

Python "input" module enhancements, such as combining colorama and updates to johejo's "inputimeout" library.

<img src="static/elf_enters_input_to_chat.jpeg" alt="enter into an input" width=400 />

###### Image created by Bing Image Creator (Dall-e 3)

This repo was based off [johenjo's `inputtimeout`](https://github.com/johejo/inputimeout/tree/master) implementation. However, since that repo is a public archive, and there are other ways I want to handle timed-out inputs, I decided to create my own variation. In addition, this repo library also includes the employment of [`colorama`](https://pypi.org/project/colorama/) as optional styling. (Currently, version `0.2.1` of this library only supports text color and not background colors.)

### Version `0.2.1`

---

# Installation

```sh
# Install main
pip install enhanced_input@git+ssh://git@github.com/nga-27/enhanced-input.git@main

# Specific version
pip install enhanced_input@git+ssh://git@github.com/nga-27/enhanced-input.git@v0.2.1
```

---

# Usage

```python
from enhanced_input import EnhancedInput, EnhancedInputColor

e_input = EnhancedInput()

# prompt input with default timeout (~30s)
e_input.input("What's your name? ")

# prompt input with modified timeout (5.1s)
e_input.input(">>> ", timeout=5.1)

# prompt input with modified timeout and color change (cyan)
e_input.input(">>> ", timeout=5.1, text_color=EnhancedInputColor.CYAN)

# prompt input for a password (with '*' hiding password)
e_input.input(">>>", timeout=34.0, password_mask="*")

# prompt input for a password (with all characters hiding the password)
e_input.input(">>>", timeout=34.0, password_mask="")
```
