# Juleb Product Bulk

## Overview

This module is useful for importing large amounts of master product data, with two main features:

- Download the master data template to upload. This allows you to easily create a spreadsheet containing the product data you want to import.
- Upload data from the downloaded master data template. This imports the product data from the spreadsheet into Odoo.
This module also supports the following conditions:

- If the internal reference does not exist in the system, a record will be created.
- If the internal reference exists, it will be updated.

## Prerequisites for Running an Module:

- **User Permissions**: Ensure that the user running the code has the necessary permissions to create directories and write files in the specified locations. Avoid running code with superuser privileges unless required.

- **Filesystem Permissions**: Set appropriate permissions on directories and files that the code will create or modify using the `chmod` command. Be cautious with permissions to maintain security.

- **Execute the Script**: Run the script from a terminal, using the appropriate user with necessary permissions. Make sure the directory structure and environment are set up correctly.

- **Error Handling**: Handle errors gracefully, especially I/O errors. Log or display error messages to understand and resolve issues effectively.

- **Testing Environment**: Test your code in a safe environment before deploying it in production to ensure it behaves as expected.

- **Backup Data**: If the code operates on important data, consider making backups or working in a safe environment to avoid data loss.

## Installation

1. Install Odoo: Ensure that you have Odoo installed and running. (Preferably Odoo16 CE)
2. Install Inventory Module
3. Module Installation: Install this module through the Odoo user interface or using the command-line tool.

## Usage

1. Go to the Inventory module.
2. Select the Configuration menu and scroll down to the Import Product Bulk menu.
3. In the Import Product Bulk menu, a widget (pop-up) will appear.
4. Download the Master Product Template.
5. Fill in the template with your product data, based on the column headings.
6. Save the file.
7. Upload the Excel file in the Import Product Bulk menu.
8. Click the Process Data button.
9. Wait for the process to finish.
10. You will see a notification indicating how many products were created and updated.

## Author

- Muhammad Rizqi (https://www.linkedin.com/in/muhrizqi/)