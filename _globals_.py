import plotly.io as pio
import plotly.graph_objects as go
from fredapi import Fred
fred = Fred(api_key="6050b935d2f878f1100c6f217cbe6753")

#   Meses en español
meses_espanol = {
1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
}

#__________Lista de colores____________________
red="#FF9999"
green="#90EE90"
blue="#ADD8E6"
yellow="#FFFF99"
purple="#CC99FF"
cyan="#93FFFF"
orange="#FFCC99"
pink="#FFB6C1"
gray="#C0C0C0"
black="#404040"
white="#F0F0F0"
brown="#CD853F"
olive="#C0C080"
teal="#80C0C0"
lavender="#C080C0"
salmon="#FFA07A"
maroon="#B03060"
navy="#3C3C64"
beige="#F5F5DC"
#______________________________________________

colorscale = [
    [0, '#632626'],  # Valor más bajo
    [0.25, '#FF8080'],
    [0.5, '#FFFFFF'],  # Valor medio (0)
    [0.75,'#A5DD9B'],
    [1, '#5F7161']   # Valor más alto
            ]

pio.templates["Oficial"] = go.layout.Template(
    layout_annotations=[
        dict(
            name="watermark",
            text="🧉DatArg",
            textangle=-30,
            opacity=0.1,
            font=dict(color="black", size=50),
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
    ]
)
pio.templates.default = "Oficial"


w_barra_stocks="""<!-- TradingView Widget BEGIN -->
                <div class="tradingview-widget-container">
                <div class="tradingview-widget-container__widget"></div>
                <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
                {
                "symbols": [
                    {
                    "description": "S&Y 500",
                    "proName": "AMEX:SPY"
                    },
                    {
                    "description": "NASDAQ",
                    "proName": "NASDAQ:QQQ"
                    },
                    {
                    "description": "IBOVESPA",
                    "proName": "BMFBOVESPA:IBOV"
                    },
                    {
                    "description": "YPF",
                    "proName": "NYSE:YPF"
                    },
                    {
                    "description": "Trans. Gas Sur",
                    "proName": "NYSE:TGS"
                    },
                    {
                    "description": "Galicia",
                    "proName": "NASDAQ:GGAL"
                    },
                    {
                    "description": "Banco BBVA",
                    "proName": "NYSE:BBAR"
                    },
                    {
                    "description": "Banco Macro",
                    "proName": "NYSE:BMA"
                    },
                    {
                    "description": "Banco Supervielle",
                    "proName": "NYSE:SUPV"
                    },
                    {
                    "description": "Pampa Energía",
                    "proName": "NYSE:PAM"
                    },
                    {
                    "description": "Edenor",
                    "proName": "NYSE:EDN"
                    },
                    {
                    "description": "Central Puerto",
                    "proName": "NYSE:CEPU"
                    },
                    {
                    "description": "Telecom",
                    "proName": "NYSE:TEO"
                    },
                    {
                    "description": "Cresud",
                    "proName": "NASDAQ:CRESY"
                    },
                    {
                    "description": "Loma Negra",
                    "proName": "NYSE:LOMA"
                    },
                    {
                    "description": "Tenaris",
                    "proName": "NYSE:TS"
                    },
                    {
                    "description": "Ternium",
                    "proName": "NYSE:TX"
                    },
                    {
                    "description": "Vista Energía",
                    "proName": "NYSE:VIST"
                    },
                    {
                    "description": "Mercado Libre",
                    "proName": "NASDAQ:MELI"
                    },
                    {
                    "description": "Globant",
                    "proName": "NYSE:GLOB"
                    },
                    {
                    "description": "Despegar",
                    "proName": "NYSE:DESP"
                    },
                    {
                    "description": "Oro",
                    "proName": "TVC:GOLD"
                    },
                    {
                    "description": "Plata",
                    "proName": "TVC:SILVER"
                    },
                    {
                    "description": "Cobre",
                    "proName": "CAPITALCOM:COPPER"
                    },
                    {
                    "description": "Crudo WTI",
                    "proName": "BLACKBULL:WTI"
                    },
                    {
                    "description": "Crudo Brent",
                    "proName": "BLACKBULL:BRENT"
                    },
                    {
                    "description": "Trigo",
                    "proName": "CAPITALCOM:WHEAT"
                    },
                    {
                    "description": "Soja",
                    "proName": "CAPITALCOM:SOYBEAN"
                    },
                    {
                    "description": "Maíz",
                    "proName": "CAPITALCOM:CORN"
                    }
                ],
                "showSymbolLogo": true,
                "isTransparent": true,
                "displayMode": "compact",
                "colorTheme": "white",
                "locale": "es",
                "backgroundColor": "#E8EBF3"

                }
                </script>
                </div>
                <!-- TradingView Widget END -->"""
