// See https://aka.ms/new-console-template for more information

Console.WriteLine("Podaj nazwe produktu: ");
String? prodName = Console.ReadLine();

Product product = new Product { ProductName = prodName };

ProdContext prodContext = new ProdContext();
prodContext.Products.Add(product);
prodContext.SaveChanges();

var query = from prod in prodContext.Products
    select prod.ProductName;

Console.WriteLine("Lista produktów w bazie: ");

foreach (var p in query) {
    Console.WriteLine(p);
}

Console.WriteLine("Hello, World!");
