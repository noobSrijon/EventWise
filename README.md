# EventWise: Event Registration Management System

EventWise is a comprehensive Event Registration Management System developed using Flask, a lightweight web framework in Python. This system aims to simplify the event registration process, provide efficient management tools for organizers, and enhance the overall experience for both organizers and attendees.

## Key Features

- User-friendly registration form: Attendees can easily submit their event registration details, including the payment transaction number.
- Admin panel: Organizers have access to a secure admin panel to review and confirm payments, ensuring smooth event management.
- Payment transaction tracking: The system allows organizers to track and manage payment transactions efficiently.
- SMS confirmation: Attendees receive automatic SMS confirmations upon successful registration and payment.
- Online ticket generation: EventWise generates online tickets for registered attendees, providing a convenient and paperless ticketing system.

## Getting Started

To get started with EventWise, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/EventWise.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a service account and download the JSON key file from the Google Cloud Console.

4. Copy the downloaded JSON key file to the project's root directory and rename it to `json_key_file.json`.

5. Open `app.py` and replace the `file={}` in the following line with the path to your JSON key file:

   ```python
   gc = gspread.service_account(filename='path/to/your/json_key_file.json')
   ```

6. Customize your Google Sheet:

   - Open the Google Sheet you want to use for EventWise.
   - Add the following column headers in the first row of the sheet: `Time`, `ID`, `Name`, `Roll`, `Amount`, `Payment Method`, `Transaction Number`, `Image Url`, `Email`, `Phone Number`, and `Status`.
7.Configure the application settings:
   - Update the admin panel credential configurations in `config.py`.
   - Set up the SMS gateway API credentials in `config.py` for sending SMS confirmations and you may also change the API URL with your provider's URL.
   - 
8. Run the application:

   ```bash
   python app.py
   ```

9. Access the application in your web browser at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Contributing

We welcome contributions to enhance EventWise. To contribute, please follow our [contribution guidelines](CONTRIBUTING.md).

## License

EventWise is released under the [MIT License](LICENSE).

## Contact

For any inquiries or support, please email us at srijonkumar18@gmail.com.
