import pandas as pd
from flask import (
    Flask,
    render_template,
)


# Read dataset
data = pd.read_csv("Headhunters_with_Rating.csv")

# Drop unnecessary columns & Rename to Hungarian
data.drop(
    columns=['Key', 'Postcode', 'Street', 'Office', 'TaxID'],
    inplace=True
    )
data.sort_values(by=['Rating', 'Total Ratings', 'City', 'Name'], inplace=True, ascending=[False, False, True, True])
data.columns = ['Név', 'Város', 'Értékelés', 'Google Értékelések']


app = Flask(__name__)
app.config['SECRET_KEY'] = 'nobody-gonna-guess-it'


@app.route('/')
def table():
    result_length = len(data)
    return render_template(
        "table.html", result_length=result_length, column_names=data.columns.values,
        row_data=list(data.values.tolist()), link_column="Url", zip=zip)


if __name__ == '__main__':
    app.run(ssl_context="adhoc", debug=True)
