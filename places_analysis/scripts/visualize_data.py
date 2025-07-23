import matplotlib.pyplot as plt
import seaborn as sns

def plot_top_categories(category_series, top_n=10):
    plt.figure(figsize=(8, 6))
    ax = category_series.head(top_n).plot(kind='barh', color='skyblue')
    plt.title('Top Categories')
    plt.xlabel('Count')
    plt.ylabel('Category')
    
    # Добавление лейблов на полосы
    for i, v in enumerate(category_series.head(top_n)):
        ax.text(v + 0.5, i, str(int(v)), va='center')

    plt.tight_layout()
    plt.show()

def plot_ratings_distribution(df):
    if 'rating' not in df.columns:
        print("Column 'rating' not found.")
        return

    plt.figure(figsize=(8, 5))
    sns.histplot(df['rating'].dropna(), bins=20, kde=True, color='mediumseagreen')
    plt.title('Ratings Distribution')
    plt.xlabel('Rating')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.show()

def plot_reviews_count_distribution(df):
    if 'user_ratings_total' not in df.columns:
        print("Column 'user_ratings_total' not found.")
        return

    plt.figure(figsize=(8, 5))
    sns.histplot(df['user_ratings_total'].dropna(), bins=20, kde=False, color='cornflowerblue')
    plt.title('Reviews Count Distribution')
    plt.xlabel('Number of Reviews')
    plt.ylabel('Count of Places')
    plt.tight_layout()
    plt.show()

def plot_price_level_distribution(df):
    if 'price_level' not in df.columns:
        print(f"Column 'price_level' not found. Available columns: {list(df.columns)}")
        return
    
    valid_data = df[df['price_level'].notna()]
    if len(valid_data) == 0:
        print("No valid price level data to plot.")
        return

    plt.figure(figsize=(8, 6))
    ax = sns.countplot(x='price_level', data=valid_data, palette='pastel')

    # Добавление лейблов
    for p in ax.patches:
        height = p.get_height()
        ax.text(
            p.get_x() + p.get_width() / 2.,
            height + 0.5,
            f'{int(height)}',
            ha='center', va='bottom'
        )

    plt.title('Price Level Distribution')
    plt.xlabel('Price Level')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.show()
