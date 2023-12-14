from django.shortcuts import render, HttpResponse
from .models import Asintocategory, Productmetadata, Asintosalesrank, Asintosimplecategory
from django.db.models import Count
import ast
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from elasticsearch import Elasticsearch
# Create your views here.
es = Elasticsearch([{'host': 'localhost', 'port': 9200, "scheme": "https"}],
                   basic_auth=(str('elastic'), str('IJRmyQo=s-0Hfb5h8eDh')),verify_certs=False)
from neo4j import GraphDatabase
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "abcd1234"))
import accelerate
import transformers
import json
REPO_ID = "/home/robertwang/PycharmProjects/llama/w-7b-hf"
tokenizer = transformers.LlamaTokenizer.from_pretrained(REPO_ID)

# This device map was generated using accelerator.infer_auto_device_map() function
device_map = {
    'model.embed_tokens': 0,
     'model.layers.0': 0,
     'model.layers.1': 0,
     'model.layers.2': 0,
     'model.layers.3': 0,
     'model.layers.4': 0,
     'model.layers.5': 0,
     'model.layers.6': 0,
     'model.layers.7': 0,
     'model.layers.8': 0,
     'model.layers.9': 0,
     'model.layers.10': 0,
     'model.layers.11': 0,
     'model.layers.12': 0,
     'model.layers.13': 0,
     'model.layers.14': 0,
     'model.layers.15': 0,
     'model.layers.16': 0,
     'model.layers.17': 0,
     'model.layers.18': 0,
     'model.layers.19': 0,
     'model.layers.20': 0,
     'model.layers.21': 0,
     'model.layers.22': 0,
     'model.layers.23': 0,
     'model.layers.24': 0,
     'model.layers.25': 0,
     'model.layers.26': 0,
     'model.layers.27': 0,
     'model.layers.28': 0,
     'model.layers.29': 0,
     'model.layers.30': 0,
     'model.layers.31': 0,
     'model.norm': 0,
     'lm_head': 0
}
model = transformers.LlamaForCausalLM.from_pretrained(
        REPO_ID,
        device_map=device_map,
        offload_folder="/tmp/.offload",
        load_in_8bit=True,
        llm_int8_enable_fp32_cpu_offload=True,
    )
def main_page(request):
    if request.method == "GET":
        categories = ((Asintocategory.objects.values('category_level_1')
                       .annotate(dcount=Count('category_level_1')))
                      .order_by('-dcount'))[0:12]
        img_url = []
        for category in categories:
            temp_cat = category['category_level_1']
            temp_asin = Asintocategory.objects.filter(category_level_1=temp_cat).first()
            temp_asin = temp_asin.asin
            temp_product = Productmetadata.objects.get(asin=temp_asin)
            img_url.append(temp_product.imurl)
        top_sale_asin = Asintosalesrank.objects.filter(sales_rank=1).values_list('asin', flat=True)
        top_sale_products = Productmetadata.objects.filter(asin__in=top_sale_asin)
        return render(request, 'index.html', context={'categories': categories,
                                                      'img_url': img_url,
                                                      'top_sale_products': top_sale_products})
    else:
        return HttpResponse("API get_categories function error")


def get_product_detail(request, asin):
    if request.method == "GET":

        ### asin:0014072149

        product = Productmetadata.objects.get(asin=asin)
        sale_rank = Asintosalesrank.objects.get(asin=asin)
        also_bought_list = []
        also_viewed_list = []
        bought_together_list = []
        buy_after_viewing_list = []

        temp_also_bought = product.also_bought
        temp_also_viewed = product.also_viewed
        temp_bought_together = product.bought_together
        temp_buy_after_viewing = product.buy_after_viewing

        if temp_also_bought:
            temp_also_bought = ast.literal_eval(temp_also_bought)
            for ele in temp_also_bought:
                try:
                    temp_product = Productmetadata.objects.get(asin=ele)
                    also_bought_list.append(temp_product)
                except Exception as e:
                    continue
        else:
            also_bought_list = None

        if temp_also_viewed:
            temp_also_viewed = ast.literal_eval(temp_also_viewed)
            for ele in temp_also_viewed:
                try:
                    temp_product = Productmetadata.objects.get(asin=ele)
                    also_viewed_list.append(temp_product)
                except Exception as e:
                    continue
        else:
            also_viewed_list = None

        if temp_bought_together:
            temp_bought_together = ast.literal_eval(temp_bought_together)
            for ele in temp_bought_together:
                try:
                    temp_product = Productmetadata.objects.get(asin=ele)
                    bought_together_list.append(temp_product)
                except Exception as e:
                    continue
        else:
            bought_together_list = None

        if temp_buy_after_viewing:
            temp_buy_after_viewing = ast.literal_eval(temp_buy_after_viewing)
            for ele in temp_buy_after_viewing:
                try:
                    temp_product = Productmetadata.objects.get(asin=ele)
                    buy_after_viewing_list.append(temp_product)
                except Exception as e:
                    continue
        else:
            buy_after_viewing_list = None

        SwingAsins_list = []

        cypher_query = ("match (n1:Asin {value: $asin_value}) - [r:SwingSimilarity] - (n2:Asin) return n2.value")
        records, summary, keys = driver.execute_query(cypher_query,database_="neo4j",asin_value=asin)

        for record in records:
            SwingAsins_list.append(record['n2.value'])

        SwingProducts_list = Productmetadata.objects.filter(asin__in=SwingAsins_list)[0:50]


        return render(request, 'detail.html', context={'product': product,
                                                       'sale_rank': sale_rank,
                                                       'also_bought_list': also_bought_list,
                                                       'also_viewed_list': also_viewed_list,
                                                       'bought_together_list': bought_together_list,
                                                       'buy_after_viewing_list': buy_after_viewing_list,
                                                       'SwingProducts_list':SwingProducts_list})
    else:
        return HttpResponse("API get_product_detail function error")


def search_by_category(request, search_text: str):
    if request.method == "GET":
        asin_list = Asintosimplecategory.objects.filter(category__iexact=search_text.capitalize()).values_list('asin', flat=True)
        products_list = Productmetadata.objects.filter(asin__in=asin_list)

        paginator = Paginator(products_list, 9)  # 实例化一个分页对象, 每页显示9个
        page = request.GET.get('page')  # 从URL通过get页码，如?page=3
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)  # 如果传入page参数不是整数，默认第一页
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        is_paginated = True if paginator.num_pages > 1 else False  # 如果页数小于1不使用分页
        context = {'page_obj': page_obj, 'is_paginated': is_paginated}
        return render(request, 'bycategory.html', context=context)
    else:
        return HttpResponse("API search_by_category function error")

def search_bar(request):
    if request.method == "GET":
        search_contents = request.GET.get('search_content')
        print(len(search_contents))
        if len(search_contents) > 20:
            batch = tokenizer(
                "Please extracts the mentioned product ,its category, its brand and its price in the sentence: " +
                search_contents,
                return_tensors="pt",
                add_special_tokens=False
            )
            batch = {k: v for k, v in batch.items()}
            n_input_tokens = batch["input_ids"].shape[-1]
            generated = model.generate(batch["input_ids"].to("cuda"), max_length=128)
            ans = tokenizer.decode(generated[0])
            print(ans)
            ans = ans.split('\n')
            info = {}
            for line in ans:
                # Checking if the line contains ':'
                if ':' in line:
                    # Splitting the line at ':'
                    key, value = line.split(':', 1)
                    # Cleaning and storing the data
                    info[key.strip('* ')] = value.strip()
            search_string = ("Product : " + info['Product'] + "," + "Category : " + info["Category"] + "," + "Brand : "
                             + info["Brand"])
            query = {
                "size": 9,
                "query": {
                    "multi_match": {
                        "query": search_string,
                        "fields": ["title", "brand", "categories"]
                    }
                }
            }
            response = es.search(index="products", body=query)
            target_asins = []
            for hit in response['hits']['hits']:
                target_asins.append(hit['_source']['asin'])
            target_products = Productmetadata.objects.filter(asin__in=target_asins)
            paginator = Paginator(target_products, 9)  # 实例化一个分页对象, 每页显示9个
            page = request.GET.get('page')  # 从URL通过get页码，如?page=3
            try:
                page_obj = paginator.page(page)
            except PageNotAnInteger:
                page_obj = paginator.page(1)  # 如果传入page参数不是整数，默认第一页
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            is_paginated = True if paginator.num_pages > 1 else False  # 如果页数小于1不使用分页
            context = {'page_obj': page_obj, 'is_paginated': is_paginated}
            return render(request, 'bycategory.html', context=context)
        else:
            query = {
                "size": 9,
                "query": {
                    "multi_match": {
                        "query": search_contents,
                        "fields": ["title", "brand", "categories"]
                    }
                }
            }
            response = es.search(index="products", body=query)
            target_asins = []
            for hit in response['hits']['hits']:
                 target_asins.append(hit['_source']['asin'])
            target_products = Productmetadata.objects.filter(asin__in=target_asins)
            paginator = Paginator(target_products, 9)  # 实例化一个分页对象, 每页显示9个
            page = request.GET.get('page')  # 从URL通过get页码，如?page=3
            try:
                page_obj = paginator.page(page)
            except PageNotAnInteger:
                page_obj = paginator.page(1)  # 如果传入page参数不是整数，默认第一页
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            is_paginated = True if paginator.num_pages > 1 else False  # 如果页数小于1不使用分页
            context = {'page_obj': page_obj, 'is_paginated': is_paginated}
            return render(request, 'bycategory.html', context=context)
    else:
        print(request)
        return HttpResponse("API search_bar function POST")
