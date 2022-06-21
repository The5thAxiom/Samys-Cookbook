import userStore from '../stores/userStore';
import accessTokenStore from '../stores/accessTokenStore';
import collectionStore from '../stores/collectionsStore';

export default function useFetch(): {
    fetchAsUser: (input: RequestInfo, init?: RequestInit) => Promise<Response>;
    fetchJsonAsUser: <T>(input: RequestInfo, init?: RequestInit) => Promise<T>;
    fetchJson: <T>(input: RequestInfo, init?: RequestInit) => Promise<T>;
} {
    const { accessToken, setAccessToken, removeAccessToken } =
        accessTokenStore();
    const setUser = userStore(state => state.setUser);
    const setCollections = collectionStore(state => state.setCollections);

    const fetchAsUser = async (
        input: RequestInfo,
        init?: RequestInit
    ): Promise<Response> => {
        const res = await fetch(input, {
            ...init,
            headers: {
                ...init?.headers,
                Authorization: `Bearer ${accessToken}`
            }
        });
        const response = res.clone();
        if (res.status !== 401) {
            try {
                const data = await res.json();
                if (data && data.access_token)
                    setAccessToken(data.access_token);
            } catch (e) {}
        } else {
            removeAccessToken();
            setUser(null as any);
            setCollections(null as any);
        }
        return response;
    };

    const fetchJsonAsUser = async <T>(
        input: RequestInfo,
        init?: RequestInit
    ): Promise<T> => {
        const res = await fetch(input, {
            ...init,
            headers: {
                ...init?.headers,
                Authorization: `Bearer ${accessToken}`
            }
        });
        if (res.status !== 401) {
            const data = await res.json();
            let ans = data;
            const token = data.access_token;
            if (token) {
                setAccessToken(token);
                delete ans['access_token'];
            }
            return ans as T;
        } else {
            removeAccessToken();
            setUser(null as any);
            setCollections(null as any);
            return null as any;
        }
    };

    const fetchJson = async <T>(
        input: RequestInfo,
        init?: RequestInit
    ): Promise<T> => {
        const res = await fetch(input, init);
        const data = await res.json();
        return data as T;
    };

    return {
        fetchAsUser,
        fetchJsonAsUser,
        fetchJson
    };
}

