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

```
git clone https://github.com/noobSrijon/EventWise.git
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Configure the application settings:

   - Update the database configurations in `config.py`.
   - Set up the SMS gateway API credentials in `config.py` for sending SMS confirmations.

4. Run the application:

```
python app.py
```

5. Access the application in your web browser at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

For detailed documentation and usage examples, refer to the [Wiki](https://github.com/noobSrijon/EventWise/wiki) section.

## Contributing

We welcome contributions to enhance EventWise. To contribute, please follow our [contribution guidelines](CONTRIBUTING.md).

## License

EventWise is released under the [MIT License](LICENSE).

## Contact

For any inquiries or support, please email us at srijonkumar18@gmail.com.
