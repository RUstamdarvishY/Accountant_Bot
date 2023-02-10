from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from db_api.models import list_all_categories


plt.style.use('ggplot')

x1 = [i for i in list_all_categories('expense')]
y1 = [i for i in list_all_categories('time')]

slices = [i for i in list_all_categories('expense')]
labels = [i for i in list_all_categories['name']]


fig1, axis1 = plt.subplots(nrows=1, ncols=1)
fig2, axis2 = plt.subplots(nrows=1, ncols=1)


axis1.plot(x1, y1, linewidth=3, label='')
axis1.legend()
axis1.set_title('Расходы на временной линии')
axis1.set_xlabel('Расходы')
axis1.set_ylabel('Время')


axis2.pie(slices, labels=labels, wedgeprops={'edgecolor': 'black'},
          shadow=True, autopct='%1.1f%%')
axis2.legend()
axis2.set_title('Расходы по категориям')


plt.show()

def save_image(filename):
    p = PdfPages(filename)
      
    fig_nums = plt.get_fignums()  
    figs = [plt.figure(n) for n in fig_nums]
      
    for fig in figs: 
        fig.savefig(p, format='pdf') 
      
    p.close()  


save_image('graphs.pdf')