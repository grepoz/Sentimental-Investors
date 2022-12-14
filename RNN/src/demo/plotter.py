# from datetime import datetime, timedelta
#
# import matplotlib.pyplot as plt
# import numpy as np
# import seaborn as sns
#
# from data_master.data_manager import DataManager
#
#
# class Plotter:
#
#     def __init__(self, data_manager):
#         self.data_manager = data_manager
#
#     def calc_date_range(self):
#         start_date_time_obj = datetime.fromisoformat(self.data_manager.start_time)
#         end_date_time_obj = datetime.fromisoformat(self.data_manager.end_time)
#         return start_date_time_obj, end_date_time_obj
#
#     @staticmethod
#     def date_range_to_str(start_date_time_obj, end_date_time_obj):
#         return str(start_date_time_obj.date()) + " - " + str(end_date_time_obj.date())
#
#     @staticmethod
#     def date_range_as_list_to_str(date_range):
#         return str(date_range[0].date()) + " - " + str(date_range[1].date())
#
#     def calc_date_range_for_train_set(self):
#         start_date_time_obj, end_date_time_obj = self.calc_date_range()
#         delta = end_date_time_obj - start_date_time_obj
#         delta = int(np.round(DataManager.ratio_of_sets * delta.days))
#         end_date_time_obj = end_date_time_obj - timedelta(days=delta)
#         return Plotter.date_range_to_str(start_date_time_obj, end_date_time_obj)
#
#     def calc_date_range_for_train_set_raw_dates(self):
#         start_date_time_obj, end_date_time_obj = self.calc_date_range()
#         delta = end_date_time_obj - start_date_time_obj
#         delta = int(np.round(DataManager.ratio_of_sets * delta.days))
#         end_date_time_obj = end_date_time_obj - timedelta(days=delta)
#         return start_date_time_obj, end_date_time_obj
#
#     def calc_date_range_for_test_set(self):
#         start_date_time_obj, end_date_time_obj = self.calc_date_range()
#         delta = end_date_time_obj - start_date_time_obj
#         delta = int(np.round(DataManager.ratio_of_sets * delta.days))
#         start_date_time_obj = end_date_time_obj - timedelta(days=delta)
#         return Plotter.date_range_to_str(start_date_time_obj, end_date_time_obj)
#
#     @staticmethod
#     def single_plot(x, y=None, title='A single plot'):
#         fig, ax = plt.subplots()
#
#         if y is None:
#             ax.plot(x)
#         else:
#             ax.plot(x, y)
#
#         ax.set_title(title)
#         plt.show()
#
#     def create_plot_lookback_name(self, min_nr_of_samples="", max_nr_of_samples="", num_layers=""):
#         return "charts/" + \
#                self.data_manager.compose_filename() + "_" + \
#                "lookback_" + str(min_nr_of_samples) + "_" + str(max_nr_of_samples) + \
#                "_layers_" + str(num_layers) + \
#                ".png"
#
#     def create_plot_hidden_dimensions_name(self, min_nr_of_hidden_dims="", max_nr_of_hidden_dims=""):
#         return "charts/" + \
#                self.data_manager.compose_filename() + \
#                "_hidden_dims_" + str(min_nr_of_hidden_dims) + "_" + str(max_nr_of_hidden_dims) + \
#                ".png"
#
#     def plot_scores_for_lookbacks(self, list_to_plot, list_legends, min_nr_of_samples, max_nr_of_samples, num_layers):
#         fig, ax = plt.subplots()
#         for i in range(len(list_to_plot)):
#             ax.plot(list(range(min_nr_of_samples, max_nr_of_samples)), list_to_plot[i], label=list_legends[i])
#
#         title = "Stock: " + self.data_manager.ticker + ", " + Plotter.date_range_as_list_to_str(self.calc_date_range())
#         ax.set_title(title)
#         plt.legend(loc="upper left")
#         ax.set_xlabel("value of lookback", size=14)
#         ax.set_ylabel("score (RMSE)", size=14)
#         plt.savefig(self.create_plot_lookback_name(min_nr_of_samples, max_nr_of_samples, num_layers))
#         plt.show()
#
#     def plot_scores_for_hidden_dimensions(self, list_to_plot, list_legends,
#                                           min_nr_of_hidden_dims, max_nr_of_hidden_dims):
#         fig, ax = plt.subplots()
#         for i in range(len(list_to_plot)):
#             ax.plot(list(range(min_nr_of_hidden_dims, max_nr_of_hidden_dims)), list_to_plot[i], label=list_legends[i])
#
#         title = "Stock: " + self.data_manager.ticker + ", " + Plotter.date_range_as_list_to_str(self.calc_date_range())
#         ax.set_title(title)
#         plt.legend(loc="upper left")
#         ax.set_xlabel("nr of hidden dimensions", size=14)
#         ax.set_ylabel("score (RMSE)", size=14)
#         plt.savefig(self.create_plot_hidden_dimensions_name(min_nr_of_hidden_dims, max_nr_of_hidden_dims))
#         plt.show()
#
#     def plot_charts(self, original, predict, y_train_pred_epoch, hist, y_test, y_test_pred):
#
#         sns.set_style("darkgrid")
#         fig, axs = plt.subplots(2, 2)
#         fig.subplots_adjust(hspace=0.1, wspace=0.1)
#         plt.suptitle("LSTM", size=22, fontweight='bold')
#
#         """Training with pred. results pre epochs"""
#
#         # TODO ? change x axis values to dates
#         # sdate, edate = self.calc_date_range_for_train_set_raw_dates()
#         # date_r = pd.date_range(sdate, edate - timedelta(days=1), freq='B')
#
#         axs[0, 0].plot(original.index, original[0], label="Data", color='royalblue')
#         axs[0, 0].plot(predict.index, predict[0], label="Prediction", color='tomato')
#         # for el in y_train_pred_epoch:
#         #    axs[0, 0].plot(el.index, el[0], label="Training Prediction (LSTM)", color='yellow', alpha=0.05)
#
#         axs[0, 0].set_title('Training', size=14, fontweight='bold')
#
#         axs[0, 0].set_xlabel(self.calc_date_range_for_train_set(), size=14)
#         axs[0, 0].set_ylabel("Cost (USD)", size=14)
#         axs[0, 0].set_xticklabels('', size=10)
#         axs[0, 0].legend(loc="upper left")
#
#         """Training loss"""
#         axs[0, 1].plot(hist, color='royalblue')
#         axs[0, 1].set_xlabel("Epoch", size=14)
#         axs[0, 1].set_ylabel("Loss", size=14)
#         axs[0, 1].set_title("Training Loss (MSE)", size=14, fontweight='bold')
#
#         axs[1, 0].plot(y_test, label="Data", color='royalblue')
#         axs[1, 0].plot(y_test_pred, label="Prediction", color='tomato')
#         axs[1, 0].set_title('Test', size=14, fontweight='bold')
#         axs[1, 0].set_xlabel(self.calc_date_range_for_test_set(), size=14)
#         axs[1, 0].set_ylabel("Cost (USD)", size=14)
#         axs[1, 0].set_xticklabels('', size=10)
#         axs[1, 0].legend(loc="upper left")
#
#         """absolute error"""
#
#         test_absolute_error_per_day = []
#         # for i in range(len(y_test_pred)):
#         #     test_absolute_error_per_day.append(abs(y_test_pred[i] - y_test[i]))
#
#         axs[1, 1].plot([1, 2, 3], color='royalblue')  # test_absolute_error_per_day
#         axs[1, 1].set_xlabel(self.calc_date_range_for_test_set(), size=14)
#         axs[1, 1].set_ylabel("Error", size=14)
#         axs[1, 1].set_title("Test - absolute error", size=14, fontweight='bold')
#         axs[1, 1].set_xticklabels('', size=10)
#
#         fig.tight_layout()
#         fig.set_figheight(10)
#         fig.set_figwidth(16)
#
#         plot_name = "charts/" + self.data_manager.compose_filename() + "_4_plots" + ".png"
#         # plt.savefig(plot_name)
#         plt.show()
