import pandas as pd
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
def filter_columns(df):
    """필요한 컬럼만 선택 (일반가구원 관련 컬럼)"""
    columns_to_keep = ['행정구역별(시군구)', '시점', '성별', '연령별', '일반가구원']
    df_filtered = df[columns_to_keep].copy()
    
    print("\n" + "=" * 60)
    print("필터링 후 데이터")
    print("=" * 60)
    print(f"컬럼 수: {len(df_filtered.columns)}")
    print(f"컬럼: {df_filtered.columns.tolist()}")
    
    return df_filtered

def print_df_statistics(df, key):
    print("\n" + "=" * 60)
    print(f"{key} 기준 일반가구원 통계 요약 (2015-2024)")
    print("=" * 60)
    
    df_tmp = df[['시점', key, '일반가구원']]

    
    print(df_tmp.groupby('시점')['일반가구원'].describe())


def plot_age_gender_graph(df, ax):
    age_groups = ["15세미만", "15~19세", "20~24세", "25~29세", "30~34세", 
                  "35~39세", "40~44세", "45~49세", "50~54세", "55~59세", 
                  "60~64세", "65~69세", "70~74세", "75~79세", "80~84세", "85세이상"]

    df_filtered = df[['시점', '성별', '연령별', '일반가구원']].copy()
    
    df_gender_age = df_filtered[
        (df_filtered['성별'].isin(['남자', '여자'])) & 
        (df_filtered['연령별'].isin(age_groups))
    ].copy()
    
    df_gender_age = df_gender_age.drop_duplicates(subset=['시점', '성별', '연령별'])
    
    df_gender_age['Label'] = df_gender_age['성별'] + '-' + df_gender_age['연령별']
    
    df_pivot = df_gender_age.pivot(index='시점', columns='Label', values='일반가구원')
    
    age_colors = {
        '15세미만': '#8B4513', '15~19세': '#FF6B6B', '20~24세': '#4ECDC4', '25~29세': '#45B7D1',
        '30~34세': '#96CEB4', '35~39세': '#FFEAA7', '40~44세': '#DFE6E9', '45~49세': '#74B9FF',
        '50~54세': '#A29BFE', '55~59세': '#FD79A8', '60~64세': '#FDCB6E', '65~69세': '#6C5CE7',
        '70~74세': '#00B894', '75~79세': '#00CEC9', '80~84세': '#E17055', '85세이상': '#2D3436'
    }
    
    selected_ages = ['15세미만', '20~24세', '30~34세', '40~44세', 
                     '50~54세', '60~64세', '70~74세', '80~84세']
    
    age_display = {
        '15세미만': '<15',
        '20~24세': '20~24',
        '30~34세': '30~34',
        '40~44세': '40~44',
        '50~54세': '50~54',
        '60~64세': '60~64',
        '70~74세': '70~74',
        '80~84세': '80~84'
    }

    for age in selected_ages:
        color = age_colors.get(age, '#000000')
        display_age = age_display.get(age, age)

        male_label = f'남자-{age}'
        if male_label in df_pivot.columns:
            ax.plot(df_pivot.index, df_pivot[male_label], 
                   marker='o', linewidth=2.5, markersize=6, 
                   linestyle='-', label=f'Male {display_age}', 
                   color=color, alpha=0.8)
        
        female_label = f'여자-{age}'
        if female_label in df_pivot.columns:
            ax.plot(df_pivot.index, df_pivot[female_label], 
                   marker='s', linewidth=2, markersize=5, 
                   linestyle='--', label=f'Female {display_age}', 
                   color=color, alpha=0.6)
    
    ax.set_title('Household Members Trend by Gender and Age Group (2015-2024)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Household Members', fontsize=12, fontweight='bold')
    ax.legend(fontsize=8, loc='best', ncol=2, framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000000:.1f}M'))


def main():
    try:
        df = pd.read_csv('polulation.csv')
        
        print_df_statistics(df, '성별')
        print_df_statistics(df, '연령별')

        fig, ax = plt.subplots(figsize=(18, 10))
        plot_age_gender_graph(df, ax)
        plt.tight_layout()
        plt.show()
        
    except (FileNotFoundError, IOError):
        print("Invalid File")

    except Exception:
        print('Process Error.')

if __name__ == '__main__':
    main()