from PredictionPlotter import predict_and_plot_all

postcode_prefixes = [  'E14', 'SW19', 'SW11', 'SW18', 'E17', 'SW6', 'SW16', 'SW17', 'N1',
                       'SW15', 'SE1', 'NW6', 'W2', 'NW3', 'E4', 'W4', 'SE18', 'NW10', 'E6',
                       'W5', 'SE9', 'NW2', 'SW2', 'SE16', 'E11', 'W14', 'SW4', 'W9', 'E1',
                       'SW12', 'SE6', 'SE13', 'NW1', 'W3', 'E3', 'NW9', 'N16', 'N8', 'N4',
                       'SE25', 'SE15', 'SW3', 'N9', 'NW8', 'SE3', 'SW20', 'E16', 'SE23',
                       'SE22', 'W6', 'N7', 'N17', 'W13', 'W12', 'N22', 'SW8', 'SE10', 'E2',
                       'SE19', 'E15', 'SW7', 'SE5', 'E10', 'E7', 'SE26', 'W8', 'W11',
                       'SE28', 'N10', 'NW4', 'N11', 'SW9', 'N13', 'NW11', 'SW10', 'N12',
                       'E5', 'W7', 'N14', 'N21', 'E8', 'SE12', 'N5', 'SE4', 'E13', 'N15',
                       'NW7', 'SW1V', 'N3', 'N6', 'N19', 'SE20', 'N2', 'SW14', 'E18',
                       'SW5', 'E1W', 'E12', 'SW13', 'N18', 'E9', 'SE27', 'SE8', 'NW5',
                       'SE24', 'SE14', 'W10', 'N20', 'SW1P', 'SE2', 'SE21', 'SE7', 'SE11',
                       'SW1X', 'SE17', 'EC1V', 'W1H', 'SW1W', 'EC2Y', 'W1U', 'nan', 'WC1H',
                       'EC1R', 'W1K', 'W1W', 'W1G', 'W1T', 'WC1X', 'EC1M', 'WC1N', 'EC1Y',
                       'W1J', 'EC1A', 'EC2A', 'WC2H', 'EC1N', 'SW1H', 'EC4V', 'WC2B',
                       'WC2N', 'SW1E', 'WC1B', 'W1F', 'EC4A', 'WC1E', 'SW1Y', 'WC2E',
                       'W1B', 'W1D', 'SW1A', 'EC3N', 'WC1R', 'WC1A', 'EC4Y', 'W1S', 'WC2R',
                       'EC3R', 'EC4R', 'EC4M', 'WC1V', 'EC2M', 'N1C', 'EC3A', 'W1N', 'W1P',
                        'EC3V', 'TW4', 'W1Y', 'W1M', 'WC2A', 'IG8', 'HA2', 'EN3', 'EC2R',
                        'W1X', 'EC2V', 'W1V', 'W1R', 'W1C', 'EC4N', 'EC3M', 'EN5', 'TW10',
                        'IG1', 'EN4', 'HA5'  ]

for i in range(0, 5426):
    predict_and_plot_all("landreg", i, "")

for pc in postcode_prefixes:
    predict_and_plot_all("landreg", pc, "")
