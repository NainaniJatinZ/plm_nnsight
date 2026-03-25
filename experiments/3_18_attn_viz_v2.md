We want to improve the attention plots in @attn_viz_app.py

- the attn plots have really bad resolution 
- they are stacked horizontally 
- color scheme and scales are not good

You can check how @scripts/cache_full_seq_attention.py  and @scripts/plot_attention_heads.py are doing it. I like the coloring, scale and stuff of it more. And maybe we can have each plot as a separate thing, so we can use streamlit to zoom into each. 

Right now, we are showing the number of cells below, but i think that might be showing the number of cells with non zero attr or something? cause its >100k sometimes. Maybe we can show the number of cells that are part of the circuit? if not we can cutoff at the top 2k cells and show how many of the cells in the selected head are in the top. 

