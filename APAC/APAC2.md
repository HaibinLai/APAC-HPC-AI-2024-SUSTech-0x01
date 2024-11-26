
```C
if (is2D)  {  
    ny = nranks;  
    nz = 1;  
}  
else  {  
    ny = 1;  
    nz = nranks;  
}  
  
for (unsigned int nx_try = 1; nx_try <= nranks; nx_try++)  {  
    if (nx_in != 0 && nx_try != nx_in)  
        continue;  
    for (unsigned int ny_try = 1; nx_try * ny_try <= nranks; ny_try++)  
        {  
        if (ny_in != 0 && ny_try != ny_in)  
            continue;  
        for (unsigned int nz_try = 1; nx_try * ny_try * nz_try <= nranks;nz_try++{ 
            if (nz_in != 0 && nz_try != nz_in)  
                continue;  
            if (nx_try * ny_try * nz_try != nranks)  
                continue;  
            if (is2D && nz_try > 1)  
                continue;  
            double surface_area;  
            if (is2D)  {  
                surface_area = L.x * (ny_try - 1) + L.y * (nx_try - 1);  
			}  
            else  {  
                surface_area = L.x * L.y * (double)(nz_try - 1)  
                               + L.x * L.z * (double)(ny_try - 1)  
                               + L.y * L.z * (double)(nx_try - 1);  
            }  
            if (surface_area < min_surface_area || !found_decomposition)  {  
                nx = nx_try;  
                ny = ny_try;  
                nz = nz_try;  
                min_surface_area = surface_area;  
                found_decomposition = true;  
            }  
        }  
    }  
}
```


$$
S= L.x \times L.y \times (n_{z_{try}} - 1)  
                               + L.x \times L.z \times (n_{y_{try}} - 1)  
                               + L.y \times L.z \times (n_{x_{try}} - 1) 

$$