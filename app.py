import os
from flask import Flask, render_template, request
from montecarlo import monte_carlo_predict

app = Flask(__name__)

# Format angka → 3750112 → "3,750,112"
def format_number(x):
    return f"{x:,}"

@app.route("/", methods=["GET", "POST"])
def index():
    target_year = None
    hasil_tahun = None
    data_history = None
    data_prediksi = None

    if request.method == "POST":
        try:
            target_year = int(request.form.get("target_year"))
        except:
            target_year = None

        if target_year:
            years, values, df = monte_carlo_predict(target_year)

            # data historis
            data_history = [
                {
                    "Tahun": int(r["Tahun"]),
                    "Jumlah_Penduduk": format_number(r["Jumlah_Penduduk"])
                }
                for r in df.to_dict(orient="records")
            ]

            # data prediksi (pastikan tipe int biasa agar tojson tidak gagal)
            data_prediksi = [
                {"Tahun": int(years[i]), "Jumlah": format_number(values[i])}
                for i in range(len(years))
            ]

            # hasil tahun tujuan (angka terakhir)
            hasil_tahun = {
                "tahun": years[-1],
                "jumlah": format_number(values[-1])
            }

    return render_template(
        "index.html",
        data_history=data_history,
        data_prediksi=data_prediksi,
        hasil_tahun=hasil_tahun
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
