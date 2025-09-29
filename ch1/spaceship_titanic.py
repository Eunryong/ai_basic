
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def plot_age_group_analysis(data):
    analysis_data = data.copy()
    
    def get_age_group(age):
        if pd.isna(age):
            return None
        if age < 10:
            return '10대 미만'
        elif age < 20:
            return '10대'
        elif age < 30:
            return '20대'
        elif age < 40:
            return '30대'
        elif age < 50:
            return '40대'
        elif age < 60:
            return '50대'
        elif age < 70:
            return '60대'
        else:
            return '70대 이상'
    
    analysis_data['AgeGroup'] = analysis_data['Age'].apply(get_age_group)
    
    valid_data = analysis_data[analysis_data['AgeGroup'].notna()].copy()
    
    age_analysis = valid_data.groupby('AgeGroup')['Transported'].agg([
        ('전체', 'count'),
        ('Transported', 'sum'),
        ('Not_Transported', lambda x: (~x).sum()),
        ('전송율', lambda x: x.mean() * 100)
    ]).reset_index()
    
    age_order = ['10대 미만', '10대', '20대', '30대', '40대', '50대', '60대', '70대 이상']
    age_analysis['AgeGroup'] = pd.Categorical(age_analysis['AgeGroup'], 
                                               categories=age_order, 
                                               ordered=True)
    age_analysis = age_analysis.sort_values('AgeGroup').reset_index(drop=True)
    
    print("\n" + "=" * 60)
    print("나이대별 Transported 분석")
    print("=" * 60)
    print(age_analysis.to_string(index=False))
    
    # 그래프 생성
    fig, axes = plt.subplots(2, 1, figsize=(14, 12))
    
    # 그래프 1: 막대 그래프 (Transported vs Not Transported)
    ax1 = axes[0]
    x = np.arange(len(age_analysis))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, age_analysis['Transported'], width, 
                    label='Transported', color='#3b82f6', alpha=0.8)
    bars2 = ax1.bar(x + width/2, age_analysis['Not_Transported'], width,
                    label='Not Transported', color='#ef4444', alpha=0.8)
    
    ax1.set_xlabel('나이대', fontsize=12, fontweight='bold')
    ax1.set_ylabel('인원 수 (명)', fontsize=12, fontweight='bold')
    ax1.set_title('나이대별 Transported 현황 비교', fontsize=14, fontweight='bold', pad=20)
    ax1.set_xticks(x)
    ax1.set_xticklabels(age_analysis['AgeGroup'], rotation=45, ha='right')
    ax1.legend(fontsize=11)
    ax1.grid(axis='y', alpha=0.3)
    
    # 막대 위에 값 표시
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=9)
    
    ax2 = axes[1]
    ax2.plot(age_analysis['AgeGroup'], age_analysis['전송율'], 
             marker='o', linewidth=3, markersize=10, color='#8b5cf6')
    ax2.fill_between(range(len(age_analysis)), age_analysis['전송율'], 
                      alpha=0.3, color='#8b5cf6')
    
    ax2.set_xlabel('나이대', fontsize=12, fontweight='bold')
    ax2.set_ylabel('전송율 (%)', fontsize=12, fontweight='bold')
    ax2.set_title('나이대별 Transported 전송율', fontsize=14, fontweight='bold', pad=20)
    ax2.set_xticklabels(age_analysis['AgeGroup'], rotation=45, ha='right')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='50% 기준선')
    ax2.legend(fontsize=11)
    
    for i, row in age_analysis.iterrows():
        ax2.text(i, row['전송율'] + 2, f"{row['전송율']:.1f}%", 
                 ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('나이대별_Transported_분석.png', dpi=300, bbox_inches='tight')
    print("\n그래프가 '나이대별_Transported_분석.png'로 저장되었습니다.")
    
    return age_analysis

def find_strongest_correlation(data):
    analysis_data = data.copy()
    analysis_data['Transported'] = analysis_data['Transported'].astype(int)
    
    bool_columns = analysis_data.select_dtypes(include='bool').columns
    for col in bool_columns:
        analysis_data[col] = analysis_data[col].astype(int)
    
    analysis_results = []
    
    correlation_matrix = analysis_data.corr(numeric_only=True)
    transported_corr = correlation_matrix['Transported'].drop('Transported')

    for col, corr_value in transported_corr.items():
        analysis_results.append([col, 'numeric', corr_value])
    
    categorical_cols = ['HomePlanet', 'CryoSleep', 'Destination', 'VIP']
    for col in categorical_cols:    
        if col not in bool_columns:
            if col in analysis_data.columns and col not in bool_columns:
            # 결측치 제거하고 분석
                valid_data = analysis_data[analysis_data[col].notna()]
                
                if len(valid_data) > 0:
                    grouped_data = valid_data.groupby(col)['Transported'].mean()
                    for category_value, transport_rate in grouped_data.items():
                        analysis_results.append([col, str(category_value), transport_rate])

    results_df = pd.DataFrame(analysis_results, columns=['Feature', 'Category/Value', 'Correlation/Rate'])

    corr_result_df = results_df.sort_values(by='Correlation/Rate', ascending=False)
    print(corr_result_df)

    return corr_result_df


def merge_data(train, test):
    merged_data = pd.concat([train, test], ignore_index=True)

    print(merged_data.shape)
    print(len(merged_data))

    return merged_data


def main():
    try:
        train = pd.read_csv('train.csv')
        test = pd.read_csv('test.csv')
        
        merged_data = merge_data(train, test)
        
        find_strongest_correlation(train)

        plot_age_group_analysis(train)
    
    except (FileNotFoundError, IOError):
        print("Invalid File")

    except Exception:
        print('Process Error.')

if __name__ == '__main__':
    main()