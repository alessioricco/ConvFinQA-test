from experiments.openai_chat_gpt import _format_table

def test_format_table():
    table_data = [
        ["Header1", "Header2"],
        ["Row1Col1", "Row1Col2"],
        ["Row2Col1", "Row2Col2"]
    ]

    expected_output = "**Financial Data Overview**:\n" \
                      "| Header1 | Header2 |\n" \
                      "| Row1Col1 | Row1Col2 |\n" \
                      "| Row2Col1 | Row2Col2 |\n"

    assert _format_table(table_data) == expected_output
