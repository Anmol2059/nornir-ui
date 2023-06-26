# 🌐 Network Details UI

This UI allows you to easily retrieve your network details. It has been developed using [Nornir](https://nornir.readthedocs.io/) and [Netmiko](https://github.com/ktbyers/netmiko), and the frontend is powered by [Flask](https://flask.palletsprojects.com/) and AJAX.

## Usage Instructions

1. Fill in the required fields for group and host configurations.
2. Click the **Save Configuration** button to save the settings.
3. To retrieve Nornir data, click the **Get Nornir Data** button.
4. The Nornir data will be displayed below as a JSON object.
5. Use the **View Hosts YAML** and **View Groups YAML** buttons to view the YAML data for hosts and groups, respectively.




## UI Code

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Inventory Configuration</title>
    <link rel="stylesheet" href="style.css" />
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" />

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
      // JavaScript code here
    </script>
  </head>
  <body>
    <!-- HTML code here -->
  </body>
</html>
