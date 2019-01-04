#!/usr/bin/env python
# coding: utf-8

# In[3]:


import h5py


# In[12]:


my_file = h5py.File('model_start.h5', 'r')


# In[13]:


for g in my_file['model']['grid']:
    print(g)
                 


# In[14]:


list(my_file['model']['grid'])


# In[ ]:




