import { computed, reactive, ref } from "vue";
import { apiRequest } from "./api";

const token = ref(localStorage.getItem("stock_token") || "");
const currentUser = ref(readJson("stock_user"));
const isLoading = ref(false);
const authError = ref("");
const globalMessage = reactive({ type: "", text: "" });

const loginForm = reactive({ username: "", password: "" });
const categoryForm = reactive({ name: "", description: "" });
const manufacturerForm = reactive({ name: "", description: "", address: "", license: "" });
const productForm = reactive({
  name: "",
  description: "",
  price: "",
  made_at_date: "",
  expiration_date: "",
  manufacturer: "",
  category: "",
});
const stockForm = reactive({ product: "", qty: "", user: "" });
const stockOutForm = reactive({ stockId: "", qty: "" });

const editing = reactive({
  categoryId: null,
  manufacturerId: null,
  productId: null,
  stockId: null,
});

const categories = ref([]);
const manufacturers = ref([]);
const products = ref([]);
const stocks = ref([]);

const pageInfo = reactive({
  categories: { page: 1, total_pages: 1, total_items: 0 },
  manufacturers: { page: 1, total_pages: 1, total_items: 0 },
  products: { page: 1, total_pages: 1, total_items: 0 },
  stocks: { page: 1, total_pages: 1, total_items: 0 },
});

const productFilters = reactive({
  id: "",
  name: "",
  category: "",
  sort: "default",
  page: 1,
});

const stockFilters = reactive({
  category: "",
  manufacturer: "",
  product_name: "",
  sort: "stock_id",
  page: 1,
});

const isAuthenticated = computed(() => Boolean(token.value && currentUser.value));
const isAdmin = computed(() => currentUser.value?.role === "Admin");
const stats = computed(() => [
  { label: "Categories", value: pageInfo.categories.total_items, tone: "amber" },
  { label: "Manufacturers", value: pageInfo.manufacturers.total_items, tone: "teal" },
  { label: "Products", value: pageInfo.products.total_items, tone: "ink" },
  {
    label: "Stock Units",
    value: stocks.value.reduce((sum, item) => sum + Number(item.qty || 0), 0),
    tone: "rose",
  },
]);

function readJson(key) {
  try {
    const value = localStorage.getItem(key);
    return value ? JSON.parse(value) : null;
  } catch {
    return null;
  }
}

function setMessage(type, text) {
  globalMessage.type = type;
  globalMessage.text = text;
}

function clearMessage() {
  globalMessage.type = "";
  globalMessage.text = "";
}

function resetCategoryForm() {
  categoryForm.name = "";
  categoryForm.description = "";
  editing.categoryId = null;
}

function resetManufacturerForm() {
  manufacturerForm.name = "";
  manufacturerForm.description = "";
  manufacturerForm.address = "";
  manufacturerForm.license = "";
  editing.manufacturerId = null;
}

function resetProductForm() {
  productForm.name = "";
  productForm.description = "";
  productForm.price = "";
  productForm.made_at_date = "";
  productForm.expiration_date = "";
  productForm.manufacturer = "";
  productForm.category = "";
  editing.productId = null;
}

function resetStockForm() {
  stockForm.product = "";
  stockForm.qty = "";
  stockForm.user = currentUser.value?.id || "";
  editing.stockId = null;
}

function toDatetimeLocal(value) {
  if (!value) return "";
  return new Date(value).toISOString().slice(0, 16);
}

async function withRequest(action, successText) {
  clearMessage();
  isLoading.value = true;
  try {
    await action();
    if (successText) setMessage("success", successText);
  } catch (error) {
    const details = error.payload?.details ? JSON.stringify(error.payload.details) : "";
    setMessage("error", details ? `${error.message} ${details}` : error.message);
    throw error;
  } finally {
    isLoading.value = false;
  }
}

async function login(onSuccess) {
  authError.value = "";
  clearMessage();
  isLoading.value = true;
  try {
    const response = await apiRequest("/auth/login/", {
      method: "POST",
      body: loginForm,
    });
    token.value = response.data.token;
    currentUser.value = response.data.user;
    localStorage.setItem("stock_token", token.value);
    localStorage.setItem("stock_user", JSON.stringify(currentUser.value));
    stockForm.user = currentUser.value.id;
    loginForm.password = "";
    await loadDashboard();
    setMessage("success", `Signed in as ${currentUser.value.username}.`);
    if (onSuccess) onSuccess();
  } catch (error) {
    authError.value = error.message;
  } finally {
    isLoading.value = false;
  }
}

function logout(onDone) {
  token.value = "";
  currentUser.value = null;
  localStorage.removeItem("stock_token");
  localStorage.removeItem("stock_user");
  categories.value = [];
  manufacturers.value = [];
  products.value = [];
  stocks.value = [];
  resetCategoryForm();
  resetManufacturerForm();
  resetProductForm();
  resetStockForm();
  stockOutForm.stockId = "";
  stockOutForm.qty = "";
  setMessage("success", "Session cleared.");
  if (onDone) onDone();
}

async function loadCategories(page = 1) {
  const response = await apiRequest("/categories/", {
    token: token.value,
    params: { page, page_size: 8 },
  });
  categories.value = response.data.items;
  pageInfo.categories = response.data.pagination;
}

async function loadManufacturers(page = 1) {
  const response = await apiRequest("/manufacturers/", {
    token: token.value,
    params: { page, page_size: 8 },
  });
  manufacturers.value = response.data.items;
  pageInfo.manufacturers = response.data.pagination;
}

async function loadProducts(page = productFilters.page) {
  productFilters.page = page;
  const response = await apiRequest("/products/", {
    token: token.value,
    params: {
      page,
      page_size: 10,
      id: productFilters.id,
      name: productFilters.name,
      category: productFilters.category,
      sort: productFilters.sort,
    },
  });
  products.value = response.data.items;
  pageInfo.products = response.data.pagination;
}

async function loadStocks(page = stockFilters.page) {
  stockFilters.page = page;
  const response = await apiRequest("/stocks/", {
    token: token.value,
    params: {
      page,
      page_size: 10,
      category: stockFilters.category,
      manufacturer: stockFilters.manufacturer,
      product_name: stockFilters.product_name,
      sort: stockFilters.sort,
    },
  });
  stocks.value = response.data.items;
  pageInfo.stocks = response.data.pagination;
}

async function loadDashboard() {
  await Promise.all([
    loadCategories(pageInfo.categories.page),
    loadManufacturers(pageInfo.manufacturers.page),
    loadProducts(productFilters.page),
    loadStocks(stockFilters.page),
  ]);
}

async function submitCategory() {
  const method = editing.categoryId ? "PUT" : "POST";
  const path = editing.categoryId ? `/categories/${editing.categoryId}/` : "/categories/";
  await withRequest(async () => {
    await apiRequest(path, { method, token: token.value, body: categoryForm });
    resetCategoryForm();
    await loadCategories(pageInfo.categories.page);
  }, editing.categoryId ? "Category updated." : "Category created.");
}

async function submitManufacturer() {
  const method = editing.manufacturerId ? "PUT" : "POST";
  const path = editing.manufacturerId ? `/manufacturers/${editing.manufacturerId}/` : "/manufacturers/";
  await withRequest(async () => {
    await apiRequest(path, { method, token: token.value, body: manufacturerForm });
    resetManufacturerForm();
    await loadManufacturers(pageInfo.manufacturers.page);
  }, editing.manufacturerId ? "Manufacturer updated." : "Manufacturer created.");
}

async function submitProduct() {
  const method = editing.productId ? "PUT" : "POST";
  const path = editing.productId ? `/products/${editing.productId}/` : "/products/";
  await withRequest(async () => {
    await apiRequest(path, {
      method,
      token: token.value,
      body: {
        ...productForm,
        price: Number(productForm.price),
        manufacturer: Number(productForm.manufacturer),
        category: Number(productForm.category),
      },
    });
    resetProductForm();
    await loadProducts(productFilters.page);
  }, editing.productId ? "Product updated." : "Product created.");
}

async function submitStock() {
  const method = editing.stockId ? "PUT" : "POST";
  const path = editing.stockId ? `/stocks/${editing.stockId}/` : "/stocks/";
  await withRequest(async () => {
    await apiRequest(path, {
      method,
      token: token.value,
      body: {
        product: Number(stockForm.product),
        qty: Number(stockForm.qty),
        user: Number(stockForm.user || currentUser.value.id),
      },
    });
    resetStockForm();
    await loadStocks(stockFilters.page);
  }, editing.stockId ? "Stock updated." : "Stock added.");
}

async function submitStockOut() {
  await withRequest(async () => {
    await apiRequest(`/stocks/${stockOutForm.stockId}/stock-out/`, {
      method: "POST",
      token: token.value,
      body: { qty: Number(stockOutForm.qty) },
    });
    stockOutForm.stockId = "";
    stockOutForm.qty = "";
    await loadStocks(stockFilters.page);
  }, "Stock removed.");
}

async function removeRecord(path, reload) {
  await withRequest(async () => {
    await apiRequest(path, { method: "DELETE", token: token.value });
    await reload();
  }, "Record deleted.");
}

function startCategoryEdit(item) {
  categoryForm.name = item.name;
  categoryForm.description = item.description;
  editing.categoryId = item.id;
}

function startManufacturerEdit(item) {
  manufacturerForm.name = item.name;
  manufacturerForm.description = item.description;
  manufacturerForm.address = item.address;
  manufacturerForm.license = item.license;
  editing.manufacturerId = item.id;
}

function startProductEdit(item) {
  productForm.name = item.name;
  productForm.description = item.description;
  productForm.price = item.price;
  productForm.made_at_date = toDatetimeLocal(item.made_at_date);
  productForm.expiration_date = toDatetimeLocal(item.expiration_date);
  productForm.manufacturer = item.manufacturer.id;
  productForm.category = item.category.id;
  editing.productId = item.id;
}

function startStockEdit(item) {
  stockForm.product = item.product.id;
  stockForm.qty = item.qty;
  stockForm.user = item.user.id;
  editing.stockId = item.id;
}

export function useStockApp() {
  return {
    token,
    currentUser,
    isLoading,
    authError,
    globalMessage,
    loginForm,
    categoryForm,
    manufacturerForm,
    productForm,
    stockForm,
    stockOutForm,
    editing,
    categories,
    manufacturers,
    products,
    stocks,
    pageInfo,
    productFilters,
    stockFilters,
    isAuthenticated,
    isAdmin,
    stats,
    login,
    logout,
    loadCategories,
    loadManufacturers,
    loadProducts,
    loadStocks,
    loadDashboard,
    submitCategory,
    submitManufacturer,
    submitProduct,
    submitStock,
    submitStockOut,
    removeRecord,
    startCategoryEdit,
    startManufacturerEdit,
    startProductEdit,
    startStockEdit,
    resetCategoryForm,
    resetManufacturerForm,
    resetProductForm,
    resetStockForm,
  };
}
