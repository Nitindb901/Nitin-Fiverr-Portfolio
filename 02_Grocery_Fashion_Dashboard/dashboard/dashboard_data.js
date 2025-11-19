
// Grocery + Fashion Dashboard - Interactive Data
// Auto-generated from CSV files

const dashboardData = {
    
    // Key Performance Indicators
    kpis: {
        "Total Transactions": "111,344",
        "Total Revenue (INR)": "759,312,789.67",
        "Total Profit (INR)": "202,569,853.69",
        "Average Margin (%)": "27.00",
        "Total Quantity Sold": "289,395",
        "Unique SKUs": "95,228",
        "Unique Stores": "5",
        "Fresh Stock (%)": "16.76",
        "Ageing Stock (%)": "49.87",
        "Average Transaction Value (INR)": "6,819.52",
        "Grocery Revenue (INR)": "173,656,057.18",
        "Fashion Revenue (INR)": "585,656,732.49",
        "POS1 Revenue (INR)": "454,015,765.27",
        "POS2 Revenue (INR)": "305,297,024.40",
    },
    
    // Category Performance
    categories: [
        {
            name: "Fashion",
            transactions: 44615,
            revenue: 585656732.49,
            avgRevenue: 13126.90,
            profit: 180371410.97,
            margin: 45.02,
            quantity: 89289,
            skus: 39484
        },
        {
            name: "Grocery",
            transactions: 66729,
            revenue: 173656057.18,
            avgRevenue: 2602.41,
            profit: 22198442.72,
            margin: 14.96,
            quantity: 200106,
            skus: 55744
        },
    ],
    
    // Monthly Trends
    monthlyTrends: [
        {
            month: "2024-01",
            category: "Fashion",
            transactions: 4038,
            revenue: 51780604.80,
            profit: 15978552.87,
            quantity: 8040
        },
        {
            month: "2024-01",
            category: "Grocery",
            transactions: 6046,
            revenue: 15851680.89,
            profit: 2020438.85,
            quantity: 18158
        },
        {
            month: "2024-02",
            category: "Fashion",
            transactions: 3109,
            revenue: 41016425.51,
            profit: 12625475.12,
            quantity: 6223
        },
        {
            month: "2024-02",
            category: "Grocery",
            transactions: 4616,
            revenue: 11957977.70,
            profit: 1522039.19,
            quantity: 13659
        },
        {
            month: "2024-03",
            category: "Fashion",
            transactions: 4090,
            revenue: 53979373.41,
            profit: 16630488.19,
            quantity: 8270
        },
        {
            month: "2024-03",
            category: "Grocery",
            transactions: 6145,
            revenue: 16151443.14,
            profit: 2065760.21,
            quantity: 18456
        },
        {
            month: "2024-04",
            category: "Fashion",
            transactions: 3231,
            revenue: 42914125.65,
            profit: 13218147.62,
            quantity: 6557
        },
        {
            month: "2024-04",
            category: "Grocery",
            transactions: 4610,
            revenue: 12211986.82,
            profit: 1549797.66,
            quantity: 13869
        },
        {
            month: "2024-05",
            category: "Fashion",
            transactions: 3235,
            revenue: 42580896.71,
            profit: 13045344.78,
            quantity: 6540
        },
        {
            month: "2024-05",
            category: "Grocery",
            transactions: 4869,
            revenue: 12781650.78,
            profit: 1623429.51,
            quantity: 14806
        },
        {
            month: "2024-06",
            category: "Fashion",
            transactions: 3281,
            revenue: 42508239.36,
            profit: 13065948.58,
            quantity: 6481
        },
        {
            month: "2024-06",
            category: "Grocery",
            transactions: 4900,
            revenue: 12865005.24,
            profit: 1650468.44,
            quantity: 14706
        },
        {
            month: "2024-07",
            category: "Fashion",
            transactions: 3386,
            revenue: 44338035.97,
            profit: 13626835.23,
            quantity: 6755
        },
        {
            month: "2024-07",
            category: "Grocery",
            transactions: 5016,
            revenue: 13007998.46,
            profit: 1675789.19,
            quantity: 15092
        },
        {
            month: "2024-08",
            category: "Fashion",
            transactions: 4013,
            revenue: 52801150.37,
            profit: 16277386.47,
            quantity: 8086
        },
        {
            month: "2024-08",
            category: "Grocery",
            transactions: 6020,
            revenue: 15241138.79,
            profit: 1946560.33,
            quantity: 17915
        },
        {
            month: "2024-09",
            category: "Fashion",
            transactions: 3297,
            revenue: 43288065.65,
            profit: 13336668.13,
            quantity: 6499
        },
        {
            month: "2024-09",
            category: "Grocery",
            transactions: 4921,
            revenue: 12561792.31,
            profit: 1607224.40,
            quantity: 14785
        },
        {
            month: "2024-10",
            category: "Fashion",
            transactions: 4314,
            revenue: 56569391.89,
            profit: 17360058.77,
            quantity: 8552
        },
        {
            month: "2024-10",
            category: "Grocery",
            transactions: 6504,
            revenue: 16848464.75,
            profit: 2167266.25,
            quantity: 19495
        },
        {
            month: "2024-11",
            category: "Fashion",
            transactions: 4304,
            revenue: 56686131.25,
            profit: 17528559.66,
            quantity: 8595
        },
        {
            month: "2024-11",
            category: "Grocery",
            transactions: 6525,
            revenue: 16910925.19,
            profit: 2154930.79,
            quantity: 19423
        },
        {
            month: "2024-12",
            category: "Fashion",
            transactions: 4317,
            revenue: 57194291.92,
            profit: 17677945.55,
            quantity: 8691
        },
        {
            month: "2024-12",
            category: "Grocery",
            transactions: 6557,
            revenue: 17265993.11,
            profit: 2214737.90,
            quantity: 19742
        },
    ],
    
    // Stock Ageing
    stockAgeing: [
        {
            category: "Ageing",
            transactions: 55530,
            revenue: 378359116.63,
            quantity: 144070,
            avgAge: 135.27
        },
        {
            category: "Fresh",
            transactions: 18656,
            revenue: 125235468.53,
            quantity: 48409,
            avgAge: 15.45
        },
        {
            category: "Normal",
            transactions: 37158,
            revenue: 255718204.51,
            quantity: 96916,
            avgAge: 60.36
        },
    ],
    
    // POS Comparison
    posData: [
        {
            pos: "POS1",
            store: "Store_A",
            transactions: 22301,
            revenue: 152738567.53,
            profit: 40869813.38,
            margin: 27.05,
            quantity: 57762,
            skus: 21576
        },
        {
            pos: "POS1",
            store: "Store_B",
            transactions: 22435,
            revenue: 151747695.49,
            profit: 40373335.01,
            margin: 26.95,
            quantity: 58279,
            skus: 21730
        },
        {
            pos: "POS1",
            store: "Store_C",
            transactions: 21984,
            revenue: 149529502.25,
            profit: 39858071.93,
            margin: 26.99,
            quantity: 57413,
            skus: 21327
        },
        {
            pos: "POS2",
            store: "Store_D",
            transactions: 22193,
            revenue: 153378002.65,
            profit: 40905169.02,
            margin: 26.95,
            quantity: 57769,
            skus: 21505
        },
        {
            pos: "POS2",
            store: "Store_E",
            transactions: 22431,
            revenue: 151919021.75,
            profit: 40563464.35,
            margin: 27.07,
            quantity: 58172,
            skus: 21767
        },
    ],
    
    // SubCategory Performance
    subCategories: [
        {
            category: "Fashion",
            subCategory: "Accessories",
            transactions: 11179,
            revenue: 146474199.79,
            avgRevenue: 13102.62,
            profit: 45157926.36,
            margin: 45.04,
            quantity: 22335
        },
        {
            category: "Fashion",
            subCategory: "Kids",
            transactions: 11181,
            revenue: 147103944.25,
            avgRevenue: 13156.60,
            profit: 45352331.67,
            margin: 45.07,
            quantity: 22422
        },
        {
            category: "Fashion",
            subCategory: "Men",
            transactions: 11062,
            revenue: 145374122.58,
            avgRevenue: 13141.76,
            profit: 44759102.09,
            margin: 45.06,
            quantity: 22259
        },
        {
            category: "Fashion",
            subCategory: "Women",
            transactions: 11193,
            revenue: 146704465.87,
            avgRevenue: 13106.80,
            profit: 45102050.85,
            margin: 44.90,
            quantity: 22273
        },
        {
            category: "Grocery",
            subCategory: "Dairy",
            transactions: 16892,
            revenue: 43925260.43,
            avgRevenue: 2600.36,
            profit: 5608253.29,
            margin: 14.97,
            quantity: 50552
        },
        {
            category: "Grocery",
            subCategory: "FMCG",
            transactions: 16586,
            revenue: 43184968.11,
            avgRevenue: 2603.70,
            profit: 5507898.92,
            margin: 14.89,
            quantity: 49611
        },
        {
            category: "Grocery",
            subCategory: "Snacks",
            transactions: 16746,
            revenue: 43913904.31,
            avgRevenue: 2622.35,
            profit: 5609805.84,
            margin: 14.96,
            quantity: 50486
        },
        {
            category: "Grocery",
            subCategory: "Staples",
            transactions: 16505,
            revenue: 42631924.33,
            avgRevenue: 2582.97,
            profit: 5472484.67,
            margin: 15.00,
            quantity: 49457
        },
    ],
    
    // Top 10 Brands
    topBrands: [
        {
            category: "Fashion",
            brand: "BrandF3",
            transactions: 8989,
            revenue: 119811028.82,
            profit: 36868196.72,
            margin: 44.93,
            skus: 7977
        },
        {
            category: "Fashion",
            brand: "BrandF5",
            transactions: 8993,
            revenue: 117362323.31,
            profit: 36174438.34,
            margin: 45.02,
            skus: 7951
        },
        {
            category: "Fashion",
            brand: "BrandF1",
            transactions: 8920,
            revenue: 117207155.71,
            profit: 36088577.67,
            margin: 45.05,
            skus: 7848
        },
        {
            category: "Fashion",
            brand: "BrandF2",
            transactions: 8867,
            revenue: 116444677.76,
            profit: 35963422.57,
            margin: 45.25,
            skus: 7854
        },
        {
            category: "Fashion",
            brand: "BrandF4",
            transactions: 8846,
            revenue: 114831546.89,
            profit: 35276775.67,
            margin: 44.85,
            skus: 7854
        },
        {
            category: "Grocery",
            brand: "BrandG3",
            transactions: 13523,
            revenue: 35191493.13,
            profit: 4514685.91,
            margin: 14.99,
            skus: 11292
        },
        {
            category: "Grocery",
            brand: "BrandG5",
            transactions: 13373,
            revenue: 34710198.45,
            profit: 4463579.00,
            margin: 15.01,
            skus: 11146
        },
        {
            category: "Grocery",
            brand: "BrandG1",
            transactions: 13284,
            revenue: 34605031.39,
            profit: 4440517.33,
            margin: 15.02,
            skus: 11120
        },
        {
            category: "Grocery",
            brand: "BrandG4",
            transactions: 13354,
            revenue: 34584185.92,
            profit: 4392374.18,
            margin: 14.89,
            skus: 11183
        },
        {
            category: "Grocery",
            brand: "BrandG2",
            transactions: 13195,
            revenue: 34565148.29,
            profit: 4387286.30,
            margin: 14.87,
            skus: 11003
        },
    ],
    
    // Margin Analysis
    marginAnalysis: [
        {
            category: "Fashion",
            subCategory: "Accessories",
            avgMargin: 45.04,
            minMargin: 30.01,
            maxMargin: 60.00,
            profit: 45157926.36,
            revenue: 146474199.79,
            profitMargin: 30.83
        },
        {
            category: "Fashion",
            subCategory: "Kids",
            avgMargin: 45.07,
            minMargin: 30.00,
            maxMargin: 60.00,
            profit: 45352331.67,
            revenue: 147103944.25,
            profitMargin: 30.83
        },
        {
            category: "Fashion",
            subCategory: "Men",
            avgMargin: 45.06,
            minMargin: 30.00,
            maxMargin: 60.00,
            profit: 44759102.09,
            revenue: 145374122.58,
            profitMargin: 30.79
        },
        {
            category: "Fashion",
            subCategory: "Women",
            avgMargin: 44.90,
            minMargin: 30.01,
            maxMargin: 60.00,
            profit: 45102050.85,
            revenue: 146704465.87,
            profitMargin: 30.74
        },
        {
            category: "Grocery",
            subCategory: "Dairy",
            avgMargin: 14.97,
            minMargin: 5.00,
            maxMargin: 25.00,
            profit: 5608253.29,
            revenue: 43925260.43,
            profitMargin: 12.77
        },
        {
            category: "Grocery",
            subCategory: "FMCG",
            avgMargin: 14.89,
            minMargin: 5.00,
            maxMargin: 25.00,
            profit: 5507898.92,
            revenue: 43184968.11,
            profitMargin: 12.75
        },
        {
            category: "Grocery",
            subCategory: "Snacks",
            avgMargin: 14.96,
            minMargin: 5.00,
            maxMargin: 25.00,
            profit: 5609805.84,
            revenue: 43913904.31,
            profitMargin: 12.77
        },
        {
            category: "Grocery",
            subCategory: "Staples",
            avgMargin: 15.00,
            minMargin: 5.00,
            maxMargin: 25.00,
            profit: 5472484.67,
            revenue: 42631924.33,
            profitMargin: 12.84
        },
    ]
};

// Export for use in HTML
if (typeof module !== 'undefined' && module.exports) {
    module.exports = dashboardData;
}
