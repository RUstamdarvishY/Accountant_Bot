from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import dates as dt
from utils.db_api.orm_func import list_categories, list_expenses_price, list_expenses_time, list_categories_partition


plt.style.use('ggplot')

x1 = list_expenses_time()
y1 = list_expenses_price()


slices = list_categories_partition()
labels = list_categories()


fig1, axis1 = plt.subplots(nrows=1, ncols=1)
fig2, axis2 = plt.subplots(nrows=1, ncols=1)


axis1.plot(x1, y1, linewidth=3)
axis1.set_title('Расходы на временной линии')
axis1.set_xlabel('Расходы')
axis1.set_ylabel('Время')

fig1.autofmt_xdate()
date_formatter = axis1.fmt_xdata = dt.DateFormatter('%m-%d')
axis1.xaxis.set_major_formatter(date_formatter)


axis2.pie(slices, labels=labels, wedgeprops={'edgecolor': 'black'},
          autopct='%1.1f%%')
axis2.set_title('Расходы по категориям')


def save_plots(filename):
    p = PdfPages(filename)

    fig_nums = plt.get_fignums()
    figs = [plt.figure(n) for n in fig_nums]

    for fig in figs:
        fig.savefig(p, format='pdf')

    p.close()
