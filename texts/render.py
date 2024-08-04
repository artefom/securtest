import os
from itertools import product
from jinja2 import Environment, FileSystemLoader
import typer

app = typer.Typer()

def srip_text(text: str) -> str:
    result = []
    last_line_empty = False

    for line in text.splitlines():
        if len(line.strip()) == 0:
            if last_line_empty:
                continue
            else:
                last_line_empty = True
        else:
            last_line_empty = False
        
        result.append(line.strip())
    return "\n".join(result)


def encode_answers(combo: tuple[bool,...]):
    # Convert boolean values to '1' or '0' and join them into a string
    binary_string = ''.join(['1' if value else '0' for value in combo])

    return binary_string


@app.command()
def render(input_jinja_file: str, output_folder: str):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load the Jinja2 template
    file_loader = FileSystemLoader(os.path.dirname(input_jinja_file))
    env = Environment(
        loader=file_loader,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(os.path.basename(input_jinja_file))

    # Generate all combinations of 6 boolean variables
    bool_combinations = list(product([True, False], repeat=6))

    # Render and save each variant
    for combo in bool_combinations:
        context = {
            'ans1': combo[0],
            'ans2': combo[1],
            'ans3': combo[2],
            'ans4': combo[3],
            'ans5': combo[4],
            'ans6': combo[5],
            'trigger': combo[5],
        }

        rendered_text = srip_text(template.render(context))

        variant_name = encode_answers(combo)

        with open(os.path.join(output_folder, f'variant{variant_name}'), 'w',
                  encoding='utf-8') as f:
            f.write(rendered_text)

    print("Rendering complete!")

if __name__ == "__main__":
    app()
