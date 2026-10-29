import os

def escape(field):
    return str(field).replace('\\', '\\\\').replace(',', '\\,')

def convert_data(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='cp932') as f_in:
            lines = f_in.readlines()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return

    with open(output_file, 'w', encoding='cp932') as f_out:
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # This is a simplified parser for the existing format.
            # It may not be perfect, but it should handle the current data.
            fields = line.split(',')
            escaped_fields = [escape(field) for field in fields]
            f_out.write(','.join(escaped_fields) + '\n')

if __name__ == '__main__':
    convert_data('C:/Users/zoosl/OneDrive/デスクトップ/課題マデ/calendar/planDateSettings.txt', 'C:/Users/zoosl/OneDrive/デスクトップ/課題マデ/calendar/planDateSettings_new.txt')
    print("Conversion complete. New file is 'C:/Users/zoosl/OneDrive/デスクトップ/課題マデ/calendar/planDateSettings_new.txt'")