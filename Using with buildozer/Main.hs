module Main where
    import Text.ParserCombinators.Parsec
    import Prelude hiding (words)

    data SpecType = Spec [SpecType] String
                  | SpecComment String
                  | SpecHead String
                  | SpecTail String
                  | SpecLine SpecType SpecType
                  deriving (Show, Eq, Ord)

    prep :: SpecType -> String
    prep (SpecLine (SpecHead h) (SpecTail t)) = h ++ "= " ++ t ++ "\n"
    prep (SpecComment c) = "#" ++ c ++ "\n"

    word :: Parser String
    word = many1 (oneOf (['A'..'Z'] ++ ['a'..'z'] ++ ['.', '*', ',', '%', '_']))

    words :: Parser String
    words = many1 (oneOf (['A'..'Z'] ++ ['a'..'z'] ++ ['.', '*', ',', '%', ' ', '(', ')', '/', '_', '-'] ++ "1234567890"))

    newlines :: Parser String
    newlines = many newline

    parseComment :: Parser SpecType
    parseComment = do
        char '#'
        c <- many (noneOf ['\n']) --words
        newlines
        return $ SpecComment c

    parseHead :: Parser SpecType
    parseHead = do
        spaces
        h <- words
        return $ SpecHead h

    parseTail :: Parser SpecType
    parseTail = do
        spaces
        t <- words 
        return $ SpecTail t

    parseLine :: Parser SpecType
    parseLine = do
        h <- parseHead
        spaces
        char '='
        spaces
        t <- parseTail
        newlines
        return $ SpecLine h t
                
    mainParser :: Parser SpecType
    mainParser = do
        string "[app]"
        newlines
        ls <- many1 ((try parseComment) <|> (try parseLine))
        string "[buildozer]"
        r <- many1 (anyChar)
        return $ Spec ls r

    main :: IO ()
    main = do
        file <- readFile "copy.spec"
        let (ls, r) = case parse mainParser "ERROR" file of
                        (Left e) -> error "ERROR"
                        (Right (Spec ls' r')) -> (ls', r')
        writeFile "copy.spec" "[app]\n"
        mapM_ (\s -> appendFile "copy.spec" (prep s)) ls