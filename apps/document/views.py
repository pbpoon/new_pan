from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import DocumentItem, Document, Category

format_list = ['png', 'jpg', 'jpeg', 'bmp']


class DocumentListView(ListView):
    model = Document
    template_name = 'document/index.html'

    def get_context_data(self, **kwargs):
        kwargs['format_list'] = format_list
        return super(DocumentListView, self).get_context_data(**kwargs)


class DocumentDetailView(DetailView):
    model = Document
    template_name = 'document/detail.html'

    def get_context_data(self, **kwargs):
        kwargs['item_list'] = self.object.item.all()
        obj = self.object
        obj.views += 1
        obj.save()
        kwargs['format_list'] = format_list
        return super(DocumentDetailView, self).get_context_data(**kwargs)


class ItemDetailView(DetailView):
    model = DocumentItem
    template_name = 'document/item_detail.html'
