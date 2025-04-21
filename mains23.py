import streamlit as st
import re

st.title("Compact Calculator")

# --- Custom Styles ---
st.markdown("""
    <style>
        .stApp {
            background: #000000 !important; /* Black background */
        }

        button[kind="secondary"] {
            font-size: 20px !important; /* Smaller font size */
            height: 50px !important; /* Shorter height */
            width: 96px !important; /* Set width to 1 inch (96px) */
            border-radius: 8px !important; /* Slightly rounded corners */
            margin: 2px 4px !important; /* Compact margin */
        }

        .result {
            font-size: 30px;
            font-weight: bold;
            color: #FFFFFF; /* White text for better visibility */
            padding-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Calculator Logic ---
class Calculator:
    def perform_operation(self, a, b, operator):
        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            if b == 0:
                raise ValueError("Division by zero is not allowed.")
            return a / b
        else:
            raise ValueError("Invalid operator.")

    def calculate(self, expression_input):
        try:
            tokens = re.findall(r'\d+|\+|\-|\*|\/', expression_input)
            if not tokens:
                return "Error: Invalid input."

            result = float(tokens[0])
            i = 1
            while i < len(tokens):
                operator = tokens[i]
                operand = float(tokens[i + 1])
                result = self.perform_operation(result, operand, operator)
                i += 2

            return round(result, 2)
        except ZeroDivisionError:
            return "Error: Division by zero."
        except ValueError as ve:
            return f"Error: {ve}"
        except Exception as e:
            return f"Error: Invalid input ({e})."

# --- Calculator UI ---
class CalculatorUI:
    def __init__(self, calculator):
        self.calculator = calculator
        if "expression" not in st.session_state:
            st.session_state.expression = ""
        if "calculated_result" not in st.session_state:
            st.session_state.calculated_result = ""

    def handle_button_click(self, value):
        if value == "C":
            st.session_state.expression = ""
            st.session_state.calculated_result = ""
        else:
            st.session_state.expression += str(value)

    def display_calculator_buttons(self):
        rows = [
            ['7', '8', '9', '+'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '*'],
            ['0', '/', 'C', '']
        ]

        icons = {
            '+': '➕',
            '-': '➖',
            '*': '✖️',
            '/': '➗',
        }

        for row in rows:
            cols = st.columns(4, gap="small")
            for key, col in zip(row, cols):
                if key:
                    display_key = icons[key] if key in icons else key
                    if col.button(display_key, key=f"btn_{key}"):
                        self.handle_button_click(key)

    def display_input_and_result(self):
        expression_input = st.text_input(
            "Enter your expression:",
            value=st.session_state.expression,
            key="expression_input"
        )

        if st.button("Calculate", key="calculate_btn"):
            result = self.calculator.calculate(expression_input)
            st.session_state.calculated_result = result

        if st.session_state.calculated_result != "":
            st.markdown(
                f"<div class='result'>Result: {st.session_state.calculated_result}</div>",
                unsafe_allow_html=True
            )

# --- Run App ---
calculator = Calculator()
calculator_ui = CalculatorUI(calculator)
calculator_ui.display_calculator_buttons()
calculator_ui.display_input_and_result()
