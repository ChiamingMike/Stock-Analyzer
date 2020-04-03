'''
Created on 2020/03/31

@author: ChiamingMike
'''

import os
import pandas
import re

from matplotlib import pyplot as plt
from matplotlib import ticker


class CovidGrapher:

    def __init__(self):
        self.folder = str()
        self.files = list()
        self.company_names = list()
        self.files_path = list()
        self.covid19_df = pandas.DataFrame()
        self.company_df = pandas.DataFrame()

        self.make_files_path()
        self.find_company_names()
        self.build_graph()

        return None

    def build_graph(self):
        file_info = dict(zip(self.company_names, self.files_path))
        for company_name, file_path in file_info.items():
            self._prepare_corona_data()
            self._prepare_company_data(company_name, file_path)
            graph_df = pandas.concat([self.covid19_df, self.company_df],
                                     axis=1,
                                     join='inner',
                                     sort=True)
            graph_df.reset_index(inplace=True)

            fig, ax1 = plt.subplots(figsize=(14, 8))
            ax2 = ax1.twinx()
            ax1.plot(graph_df['Date'],
                     graph_df[company_name],
                     linewidth=2,
                     color='limegreen',
                     linestyle='dotted',
                     marker='.',
                     markersize=8,
                     label=company_name)

            ax2.bar(graph_df['Date'],
                    graph_df['Global Confirmed'],
                    color='bisque',
                    label='Global Confirmed')

            ax1.set_zorder(2)
            ax2.set_zorder(1)

            ax1.set_xlabel('Date')
            ax1.set_ylabel('value')
            ax2.set_ylabel('Number of people')

            ax1.patch.set_alpha(0)
            ax1.grid(b=True, which='major', linestyle=':')

            ax1.legend(bbox_to_anchor=(0.15, -0.1),
                       loc='lower left',
                       borderaxespad=0)
            ax2.legend(bbox_to_anchor=(0, -0.1),
                       loc='lower left',
                       borderaxespad=0)

            ax1.yaxis.set_major_locator(ticker.MultipleLocator(50))
            ax2.xaxis.set_major_locator(ticker.MultipleLocator(7))
            ax2.yaxis.set_major_locator(ticker.MultipleLocator(50000))
            fig.tight_layout()
            # plt.show()
            file_name = f'{self.folder}_{company_name}.png'
            plt.savefig(os.path.join(os.path.dirname(
                os.path.dirname(__file__)), self.folder, file_name))

        return None

    def make_files_path(self):
        self.__find_files()
        folder_path = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), self.folder)
        self.files_path = [os.path.join(folder_path, file)
                           for file in self.files]

        return None

    def find_company_names(self):
        pattern_name = r'^(\d{8})_(\d{4})_'
        self.company_names = [re.sub(pattern_name, '', file).replace('.csv', '')
                              for file in self.files]

        return None

    def _prepare_corona_data(self):
        root = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'resorces', 'COVID-19.csv')
        self.covid19_df = pandas.read_csv(root,
                                          usecols=['Date', 'Global Confirmed'],
                                          encoding='cp932',
                                          parse_dates=['Date'])
        self.covid19_df.sort_values('Date', ascending=False, inplace=True)
        self.covid19_df.set_index('Date', inplace=True)

        return None

    def _prepare_company_data(self,
                              company_name: str,
                              file_path: str):
        self.company_df = pandas.read_csv(file_path,
                                          usecols=['日付', '終値'],
                                          encoding='cp932')
        self.company_df.rename(columns={'日付': 'Date', '終値': company_name},
                               inplace=True,)
        self.company_df['Date'] = pandas.to_datetime(
            self.company_df['Date'], format='%y/%m/%d')
        self.company_df.set_index('Date', inplace=True)

        return None

    def __find_files(self):
        pattern_folder = re.compile(r'^(\d{8})$')
        pattern_file = re.compile(r'^(\d{8})_(\d{4})_.*\.csv$')
        root = os.path.dirname(os.path.dirname(__file__))

        try:
            print('Finding target files...')
            self.folder = [folder for folder in os.listdir(
                root) if pattern_folder.match(folder)][0]

            self.files = [file for file in os.listdir(
                os.path.join(root, self.folder)) if pattern_file.match(file)]
        except Exception as e:
            print(e)
            print('Stock code doesn\'t exist.')
            print('')

        return None


if __name__ == '__main__':
    covid_grapher = CovidGrapher()
