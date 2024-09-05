import datetime
import openpyxl


def main(place_name, search_term):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Define file paths
    input_file_path = f"{place_name}_{search_term}_{timestamp}_input.xlsx"
    output_file_path = f"{place_name}_{search_term}_{timestamp}_output.xlsx"
    insta_file_path = f"{place_name}_{search_term}_{timestamp}_insta.xlsx"

    # Create Excel files and write "By Vergil1000" to the first cell
    for file_path in [input_file_path, output_file_path, insta_file_path]:
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.cell(row=1, column=1, value="By Vergil1000")
        workbook.save(file_path)

    return input_file_path, output_file_path, insta_file_path


if __name__ == "__main__":
    # Example usage
    place_name = "Varanasi"
    search_term = "Aesthetics Clinic"
    files = main(place_name, search_term)
    print("Generated files:", files)
