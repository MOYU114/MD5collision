import os


def create_files():
    # Directory to store the files
    directory = "text_files"  # You can specify a full path here
    os.makedirs(directory, exist_ok=True)

    # Initial character count and increment
    start_chars = 100
    increment = 10
    num_files = 100

    # Generate files
    for i in range(1, num_files + 1):
        file_path = os.path.join(directory, f"file_{i}.txt")
        num_chars = start_chars + (i - 1) * increment
        with open(file_path, 'w') as file:
            file.write('a' * num_chars)

    print(f"Generated {num_files} files in '{directory}' with characters ranging from {start_chars} to {num_chars}.")


if __name__ == "__main__":
    create_files()